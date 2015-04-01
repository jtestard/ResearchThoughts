## Holistic Data Access Optimization for Analytics Reports

## Apply Plan Rewriter

```
```

#### Three cases

 1. FROM clause has no joins and there is either no aggregation or aggregation + group by.
 - FROM clause may have joins.
 - Aggregations without group by are allowed.
 
 
### Introducing SQL++ RI

We change the language/data model of the rewriting to SQL++ RI (more specifically Asterix SQL++) and see what happens when we try to apply the rewriting with the new datamodel to the running example of the paper.

In terms of operator descriptions, I am using those of Asterix (those I am the most familiar with).

#### Running the example with Asterix

Data to input :

```
drop dataverse TinyTPCH if exists;
create dataverse TinyTPCH;
use dataverse TinyTPCH;

create type NationType as closed {
	nation_key : int32,
	nation_name : string
}

create type CustomerType as closed {
	cust_key : int32,
	nation_ref : int32
}

create type OrderType as closed {
	order_key : int32,
	cust_ref : int32,
	order_year : string,
	total_price : double
}

create dataset Nations(NationType) primary key nation_key;
create dataset Customers(CustomerType) primary key cust_key;
create dataset Orders(OrderType) primary key order_key;

insert into dataset Nations (
{{
{ "nation_key" : 1, "nation_name" : "Canada" },
{ "nation_key" : 2, "nation_name" : "England" },
{ "nation_key" : 3, "nation_name" : "Algeria" }
}}
);

insert into dataset Customers (
{{
{ "cust_key" : 1, "nation_ref" : 1 },
{ "cust_key" : 2, "nation_ref" : 2 },
{ "cust_key" : 3, "nation_ref" : 1 }
}}
);

insert into dataset Orders (
{{
{ "order_key" : 1, "cust_ref" : 1 , "order_year" : "2010", "total_price" : 10.0 },
{ "order_key" : 2, "cust_ref" : 2 , "order_year" : "2010", "total_price" : 15.0 },
{ "order_key" : 3, "cust_ref" : 2 , "order_year" : "2011", "total_price" : 5.0 }
}}
);

for $n in dataset Nations return $n;
for $c in dataset Customers return $c;
for $o in dataset Orders return $o;
```

Running Example Query in SQL++ RI (requires a little conversion) :

```
use dataverse TinyTPCH;

SELECT 	n.nation_key as nation_key,
		n.nation_name as nation_name,
		(
			SELECT 	order_year as order_year,
					sql-sum (
		 				( SELECT ELEMENT g.o.total_price
		 				FROM group as g )
		 			) as sum_price
			FROM 	Orders as o,
					Customers as c
			WHERE	o.cust_ref = c.cust_key and
					c.nation_ref = n.nation_key
		 GROUP BY 	o.order_year as order_year
		 ORDER BY	sql-sum (
		 				( SELECT ELEMENT g.o.total_price
		 				FROM group as g )
		 			) DESC
		 	LIMIT	3
		) as aggregates
FROM Nations as n;
```


#### Initial Logical Plan

```
distribute result [%0->$$2]
  project ([$$2])
    assign [$$2] <- [function-call: asterix:open-record-constructor, Args:[AString: {nation_key}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {nation_key}], AString: {nation_name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {nation_name}], AString: {aggregates}, %0->$$26]]
      subplan {
                aggregate [$$26] <- [function-call: asterix:listify, Args:[%0->$$21]]
                  assign [$$21] <- [function-call: asterix:open-record-constructor, Args:[AString: {order_year}, %0->$$3, AString: {sum_price}, function-call: asterix:sql-sum, Args:[%0->$$25]]]
                    subplan {
                              aggregate [$$25] <- [function-call: asterix:listify, Args:[%0->$$24]]
                                assign [$$24] <- [function-call: asterix:field-access-by-name, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$6, AString: {o}], AString: {total_price}]]
                                  unnest $$6 <- function-call: asterix:scan-collection, Args:[%0->$$16]
                                    nested tuple source
                           }
                      limit AInt32: {3}
                        order (DESC, function-call: asterix:sql-sum, Args:[%0->$$20]) 
                          subplan {
                                    aggregate [$$20] <- [function-call: asterix:listify, Args:[%0->$$19]]
                                      assign [$$19] <- [function-call: asterix:field-access-by-name, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$5, AString: {o}], AString: {total_price}]]
                                        unnest $$5 <- function-call: asterix:scan-collection, Args:[%0->$$16]
                                          nested tuple source
                                 }
                            group by ([$$3 := function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {order_year}]]) decor ([]) {
                                      aggregate [$$16] <- [function-call: asterix:listify, Args:[%0->$$4]]
                                        nested tuple source
                                   }
                              assign [$$4] <- [function-call: asterix:open-record-constructor, Args:[AString: {c}, %0->$$2, AString: {o}, %0->$$1]]
                                select (function-call: algebricks:and, Args:[function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {cust_ref}], function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {cust_key}]], function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {nation_ref}], function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {nation_key}]]])
                                  unnest $$2 <- function-call: asterix:dataset, Args:[AString: {Customers}]
                                    unnest $$1 <- function-call: asterix:dataset, Args:[AString: {Orders}]
                                      nested tuple source
             }
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {Nations}]
          empty-tuple-source
```

#### Optimized Logical Plan

```
distribute result [%0->$$2]
-- DISTRIBUTE_RESULT
  exchange 
  -- ONE_TO_ONE_EXCHANGE
    project ([$$2])
    -- STREAM_PROJECT
      assign [$$2] <- [function-call: asterix:closed-record-constructor, Args:[AString: {nation_key}, %0->$$41, AString: {nation_name}, %0->$$42, AString: {aggregates}, %0->$$26]]
      -- ASSIGN
        project ([$$42, $$41, $$26])
        -- STREAM_PROJECT
          exchange 
          -- ONE_TO_ONE_EXCHANGE
            group by ([$$30 := %0->$$48]) decor ([$$41 := %0->$$48; $$42 := %0->$$44]) {
                      aggregate [$$26] <- [function-call: asterix:listify, Args:[function-call: asterix:closed-record-constructor, Args:[AString: {order_year}, %0->$$3, AString: {sum_price}, %0->$$38]]]
                      -- AGGREGATE  |LOCAL|
                        limit AInt32: {3}
                        -- STREAM_LIMIT  |LOCAL|
                          order (DESC, %0->$$37) 
                          -- IN_MEMORY_STABLE_SORT [$$37(DESC)]  |LOCAL|
                            group by ([$$3 := %0->$$49]) decor ([]) {
                                      aggregate [$$37, $$38] <- [function-call: asterix:agg-sql-sum, Args:[%0->$$46], function-call: asterix:agg-sql-sum, Args:[%0->$$47]]
                                      -- AGGREGATE  |LOCAL|
                                        nested tuple source
                                        -- NESTED_TUPLE_SOURCE  |LOCAL|
                                   }
                            -- MICRO_PRE_CLUSTERED_GROUP_BY[$$49]  |LOCAL|
                              select (function-call: algebricks:and, Args:[function-call: algebricks:not, Args:[function-call: asterix:is-system-null, Args:[%0->$$46]], function-call: algebricks:not, Args:[function-call: asterix:is-system-null, Args:[%0->$$47]]])
                              -- STREAM_SELECT  |LOCAL|
                                nested tuple source
                                -- NESTED_TUPLE_SOURCE  |LOCAL|
                   }
            -- PRE_CLUSTERED_GROUP_BY[$$48]
              exchange 
              -- HASH_PARTITION_MERGE_EXCHANGE MERGE:[$$48(ASC), $$49(ASC)] HASH:[$$48]
                group by ([$$48 := %0->$$34; $$49 := %0->$$27]) decor ([%0->$$44]) {
                          aggregate [$$46, $$47] <- [function-call: asterix:agg-local-sql-sum, Args:[%0->$$19], function-call: asterix:agg-local-sql-sum, Args:[%0->$$19]]
                          -- AGGREGATE  |LOCAL|
                            select (function-call: algebricks:not, Args:[function-call: algebricks:is-null, Args:[%0->$$33]])
                            -- STREAM_SELECT  |LOCAL|
                              nested tuple source
                              -- NESTED_TUPLE_SOURCE  |LOCAL|
                       }
                -- PRE_CLUSTERED_GROUP_BY[$$34, $$27]
                  exchange 
                  -- ONE_TO_ONE_EXCHANGE
                    order (ASC, %0->$$34) (ASC, %0->$$27) 
                    -- STABLE_SORT [$$34(ASC), $$27(ASC)]
                      exchange 
                      -- ONE_TO_ONE_EXCHANGE
                        project ([$$34, $$19, $$33, $$27, $$44])
                        -- STREAM_PROJECT
                          exchange 
                          -- ONE_TO_ONE_EXCHANGE
                            left outer join (function-call: algebricks:eq, Args:[%0->$$35, %0->$$34])
                            -- HYBRID_HASH_JOIN [$$34][$$35]
                              exchange 
                              -- ONE_TO_ONE_EXCHANGE
                                project ([$$34, $$44])
                                -- STREAM_PROJECT
                                  assign [$$44] <- [function-call: asterix:field-access-by-index, Args:[%0->$$0, AInt32: {1}]]
                                  -- ASSIGN
                                    exchange 
                                    -- ONE_TO_ONE_EXCHANGE
                                      data-scan []<-[$$34, $$0] <- TinyTPCH:Nations
                                      -- DATASOURCE_SCAN
                                        exchange 
                                        -- ONE_TO_ONE_EXCHANGE
                                          empty-tuple-source
                                          -- EMPTY_TUPLE_SOURCE
                              exchange 
                              -- HASH_PARTITION_EXCHANGE [$$35]
                                assign [$$33] <- [TRUE]
                                -- ASSIGN
                                  project ([$$35, $$19, $$27])
                                  -- STREAM_PROJECT
                                    exchange 
                                    -- ONE_TO_ONE_EXCHANGE
                                      join (function-call: algebricks:eq, Args:[%0->$$39, %0->$$32])
                                      -- HYBRID_HASH_JOIN [$$39][$$32]
                                        exchange 
                                        -- HASH_PARTITION_EXCHANGE [$$39]
                                          project ([$$19, $$39, $$27])
                                          -- STREAM_PROJECT
                                            assign [$$19, $$27, $$39] <- [function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {3}], function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {2}], function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {1}]]
                                            -- ASSIGN
                                              project ([$$1])
                                              -- STREAM_PROJECT
                                                exchange 
                                                -- ONE_TO_ONE_EXCHANGE
                                                  data-scan []<-[$$31, $$1] <- TinyTPCH:Orders
                                                  -- DATASOURCE_SCAN
                                                    exchange 
                                                    -- ONE_TO_ONE_EXCHANGE
                                                      empty-tuple-source
                                                      -- EMPTY_TUPLE_SOURCE
                                        exchange 
                                        -- ONE_TO_ONE_EXCHANGE
                                          project ([$$35, $$32])
                                          -- STREAM_PROJECT
                                            assign [$$35] <- [function-call: asterix:field-access-by-index, Args:[%0->$$2, AInt32: {1}]]
                                            -- ASSIGN
                                              exchange 
                                              -- ONE_TO_ONE_EXCHANGE
                                                data-scan []<-[$$32, $$2] <- TinyTPCH:Customers
                                                -- DATASOURCE_SCAN
                                                  exchange 
                                                  -- ONE_TO_ONE_EXCHANGE
                                                    empty-tuple-source
```

### Conclusions 

 - It is very easy to construct the running example using the Asterix SQL++ engine.
 - Some changes are required to adapt the running example to SQL++ RI, in particular with respect to group-by.
 - The initial logical plan obtained through Asterix is (somewhat unsurprisingly) the same as that of the paper.
 - Asterix uses the denormalized-set approach in its rewriting.


 
## Email to Yannis 


Hello Yannis,

I started reading the  "Holistic Data Access Optimization for Analytics Reports” paper and the first thing that strikes me is that the semantics of the SQL++ language / data model described there are different from those of the more recent SQL++ Reference Implementation paper.

My guess regarding why the paper wasn’t submitted is the realization that the specification of the SQL++ language wasn’t complete enough at that time for a paper describing query rewritings using this language. I am thinking a worthwhile effort would be to apply the rewritings presented here using the semantics of the newer language.

What do you think?

— Jules

### Rewriting by Example

Assume following schema and data :

```
CREATE TABLE nations (
	nation_key,
	name,
);
CREATE TABLE customers (
	cust_key,
	nation_ref
);
CREATE TABLE orders (
	order_key,
	cust_ref,
	order_year,
	total_price
);
INSERT INTO nations VALUES (
	(1, "China"),
	(2, "Canada")
)
```

Given input query :

```
SELECT n.nation_key, n.name, (
	SELECT order_year, SUM(o.total_price) as sum_price
	FROM orders as o, customers as c
	WHERE o.cust_ref = c.cust_key and c.nation_ref = n.nation_key
	GROUP BY order_year
	ORDER BY sum_price
	LIMIT 3 
)
from nations as n
```

Rewriting looks like :

```
FROM  nations as n
LEFT OUTER JOIN (
	FROM 
)
```



================


## Similar stuff in Asterix 

SQL++ query :

```
use dataverse TinySocial;

select user.name as name,
(
   select element message
   from FacebookMessages as message
   where message.author-id = user.id
) as messages
from FacebookUsers as user;
```

Initial Logical Plan :

```
distribute result [%0->$$2]
  project ([$$2])
    assign [$$2] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {messages}, %0->$$8]]
      subplan {
                aggregate [$$8] <- [function-call: asterix:listify, Args:[%0->$$1]]
                  select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}], function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}]])
                    unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                      nested tuple source
             }
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

Rewritten plan (with extra optimizations) :

```
distribute result [%0->$$2]
-- DISTRIBUTE_RESULT
  exchange 
  -- ONE_TO_ONE_EXCHANGE
    project ([$$2])
    -- STREAM_PROJECT
      assign [$$2] <- [function-call: asterix:closed-record-constructor, Args:[AString: {name}, %0->$$15, AString: {messages}, %0->$$8]]
      -- ASSIGN
        project ([$$8, $$15])
        -- STREAM_PROJECT
          exchange 
          -- ONE_TO_ONE_EXCHANGE
            group by ([$$9 := %0->$$12]) decor ([$$15 := %0->$$16]) {
                      aggregate [$$8] <- [function-call: asterix:listify, Args:[%0->$$1]]
                      -- AGGREGATE  |LOCAL|
                        select (function-call: algebricks:not, Args:[function-call: algebricks:is-null, Args:[%0->$$11]])
                        -- STREAM_SELECT  |LOCAL|
                          nested tuple source
                          -- NESTED_TUPLE_SOURCE  |LOCAL|
                   }
            -- PRE_CLUSTERED_GROUP_BY[$$12]
              exchange 
              -- ONE_TO_ONE_EXCHANGE
                order (ASC, %0->$$12) 
                -- STABLE_SORT [$$12(ASC)]
                  exchange 
                  -- ONE_TO_ONE_EXCHANGE
                    project ([$$1, $$16, $$11, $$12])
                    -- STREAM_PROJECT
                      exchange 
                      -- ONE_TO_ONE_EXCHANGE
                        left outer join (function-call: algebricks:eq, Args:[%0->$$13, %0->$$12])
                        -- HYBRID_HASH_JOIN [$$12][$$13]
                          exchange 
                          -- ONE_TO_ONE_EXCHANGE
                            project ([$$16, $$12])
                            -- STREAM_PROJECT
                              assign [$$16] <- [function-call: asterix:field-access-by-index, Args:[%0->$$0, AInt32: {2}]]
                              -- ASSIGN
                                exchange 
                                -- ONE_TO_ONE_EXCHANGE
                                  data-scan []<-[$$12, $$0] <- TinySocial:FacebookUsers
                                  -- DATASOURCE_SCAN
                                    exchange 
                                    -- ONE_TO_ONE_EXCHANGE
                                      empty-tuple-source
                                      -- EMPTY_TUPLE_SOURCE
                          exchange 
                          -- HASH_PARTITION_EXCHANGE [$$13]
                            assign [$$11, $$13] <- [TRUE, function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {1}]]
                            -- ASSIGN
                              project ([$$1])
                              -- STREAM_PROJECT
                                exchange 
                                -- ONE_TO_ONE_EXCHANGE
                                  data-scan []<-[$$10, $$1] <- TinySocial:FacebookMessages
                                  -- DATASOURCE_SCAN
                                    exchange 
                                    -- ONE_TO_ONE_EXCHANGE
                                      empty-tuple-source
                                      -- EMPTY_TUPLE_SOURCE
```

Results :

```
{ "name": "WillisWynne", "messages": [ { "message-id": 5, "author-id": 6, "in-response-to": 2, "sender-location": point("34.7,90.76"), "message": " love sprint the customization is mind-blowing" } ] }
{ "name": "MargaritaStoddard", "messages": [ { "message-id": 11, "author-id": 1, "in-response-to": 1, "sender-location": point("38.97,77.49"), "message": " can't stand at&t its plan is terrible" }, { "message-id": 8, "author-id": 1, "in-response-to": 11, "sender-location": point("40.33,80.87"), "message": " like verizon the 3G is awesome:)" }, { "message-id": 10, "author-id": 1, "in-response-to": 12, "sender-location": point("42.5,70.01"), "message": " can't stand motorola the touch-screen is terrible" }, { "message-id": 2, "author-id": 1, "in-response-to": 4, "sender-location": point("41.66,80.87"), "message": " dislike iphone its touch-screen is horrible" }, { "message-id": 4, "author-id": 1, "in-response-to": 2, "sender-location": point("37.73,97.04"), "message": " can't stand at&t the network is horrible:(" } ] }

{ "name": "IsbelDull", "messages": [ { "message-id": 6, "author-id": 2, "in-response-to": 1, "sender-location": point("31.5,75.56"), "message": " like t-mobile its platform is mind-blowing" }, { "message-id": 3, "author-id": 2, "in-response-to": 4, "sender-location": point("48.09,81.01"), "message": " like samsung the plan is amazing" } ] }
{ "name": "NicholasStroh", "messages": [  ] }
{ "name": "NilaMilliron", "messages": [  ] }
{ "name": "WoodrowNehling", "messages": [ { "message-id": 14, "author-id": 9, "in-response-to": 12, "sender-location": point("41.33,85.28"), "message": " love at&t its 3G is good:)" } ] }
{ "name": "BramHatch", "messages": [ { "message-id": 12, "author-id": 10, "in-response-to": 6, "sender-location": point("42.26,77.76"), "message": " can't stand t-mobile its voicemail-service is OMG:(" }, { "message-id": 13, "author-id": 10, "in-response-to": 4, "sender-location": point("42.77,78.92"), "message": " dislike iphone the voice-command is bad:(" } ] }
{ "name": "EmoryUnk", "messages": [ { "message-id": 9, "author-id": 3, "in-response-to": 12, "sender-location": point("34.45,96.48"), "message": " love verizon its wireless is good" }, { "message-id": 1, "author-id": 3, "in-response-to": 2, "sender-location": point("47.16,77.75"), "message": " love sprint its shortcut-menu is awesome:)" } ] }
{ "name": "VonKemble", "messages": [ { "message-id": 7, "author-id": 5, "in-response-to": 15, "sender-location": point("32.91,85.05"), "message": " dislike sprint the speed is horrible" } ] }
{ "name": "SuzannaTillson", "messages": [ { "message-id": 15, "author-id": 7, "in-res
                                                    -- EMPTY_TUPLE_SOURCEponse-to": 11, "sender-location": point("44.47,67.11"), "message": " like iphone the voicemail-service is awesome" } ] }
```