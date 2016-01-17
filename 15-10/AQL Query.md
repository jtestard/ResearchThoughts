If we extend the previous example as follows :

#### AQL Query

```
use dataverse TinySocial;

    for $ts in dataset TweetMessages
    group by $uid := $ts.user.screen-name with $ts
    return {
    "user": $uid,
    "count": count($ts),
    "avg-length" : avg(for $t in $ts return string-length($t.message-text))
    };
```

Notice that for any aggregation based on numbers (such as `avg`), given the packing produced by the group-by, an explicit sub-query must be created to create a list of numbers (instead of a list of records) which can be then aggregated. In SQL++ we hide the issue with syntactic sugar.

#### Initial Logical Plan

```
1 distribute result [%0->$$8] -- |UNPARTITIONED|
2  project ([$$8]) -- |UNPARTITIONED|
3    assign [$$8] <- [function-call: asterix:open-record-constructor, Args:[AString: {user}, %0->$$1, AString: {count}, function-call: asterix:count, Args:[%0->$$7], AString: {avg-length}, function-call: asterix:avg, Args:[%0->$$13]]] -- |UNPARTITIONED|
4      subplan {
5                aggregate [$$13] <- [function-call: asterix:listify, Args:[%0->$$11]] -- |UNPARTITIONED|
6                  assign [$$11] <- [function-call: asterix:string-length, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$3, AString: {message-text}]]] -- |UNPARTITIONED|
7                    unnest $$3 <- function-call: asterix:scan-collection, Args:[%0->$$7] -- |UNPARTITIONED|
8                      nested tuple source -- |UNPARTITIONED|
9             } -- |UNPARTITIONED|
10        group by ([$$1 := function-call: asterix:field-access-by-name, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {user}], AString: {screen-name}]]) decor ([]) {
11                  aggregate [$$7] <- [function-call: asterix:listify, Args:[%0->$$2]] -- |UNPARTITIONED|
12                    nested tuple source -- |UNPARTITIONED|
13               } -- |UNPARTITIONED|
14          unnest $$2 <- function-call: asterix:dataset, Args:[AString: {TweetMessages}] -- |UNPARTITIONED|
15            empty-tuple-source -- |UNPARTITIONED|
```

The initial logical plan shows again the explicit decoupling of grouping and aggregation through the use of `listify` on lines 5 and 11, followed by a call to `count` and `avg` on line 3.

#### Optimized Plan

```
1  -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
2    project ([$$8])
3    -- STREAM_PROJECT  |PARTITIONED|
4      assign [$$8] <- [function-call: asterix:closed-record-constructor, Args:[AString: {user}, %0->$$1, AString: {count}, %0->$$16, AString: {avg-length}, %0->$$17]]
5      -- ASSIGN  |PARTITIONED|
6        exchange 
7        -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
8          group by ([$$1 := %0->$$22]) decor ([]) {
9                    aggregate [$$16, $$17] <- [function-call: asterix:agg-sum, Args:[%0->$$20], function-call: asterix:agg-global-avg, Args:[%0->$$21]]
10                    -- AGGREGATE  |LOCAL|
11                      nested tuple source
12                      -- NESTED_TUPLE_SOURCE  |LOCAL|
13                 }
14          -- PRE_CLUSTERED_GROUP_BY[$$22]  |PARTITIONED|
15            exchange 
16            -- HASH_PARTITION_MERGE_EXCHANGE MERGE:[$$22(ASC)] HASH:[$$22]  |PARTITIONED|
17              group by ([$$22 := %0->$$14]) decor ([]) {
18                        aggregate [$$20, $$21] <- [function-call: asterix:agg-count, Args:[%0->$$2], function-call: asterix:agg-local-avg, Args:[function-call: asterix:string-length, Args:[%0->$$18]]]
19                        -- AGGREGATE  |LOCAL|
20                          nested tuple source
21                          -- NESTED_TUPLE_SOURCE  |LOCAL|
22                     }
```

In the optimized plan, line 9 shows the use of the `agg-sum` and `agg-global-avg` functions on the projected fields without listify. 