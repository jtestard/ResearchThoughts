### Group By into distinct rewriting

To Yannis :

Oh yes of course, I remember from CSE 232 lectures. 

However, Asterix uses different operators for `distinct` and `group-by`, it does not rewrite `distinct`s into `group-by`s.

I looked into whether Asterix rewrites `group-by` into `distinct` on logically equivalent queries:


```
use dataverse TinySocial;

// Query 1 -- Distinct
let $x := [ 
   { "a" : 1, "b" : 1 },
   { "a" : 1, "b" : 1},
   { "a" : 2, "b" : 1},
   { "a" : 1, "b" : 1, "c": 2}
]
for $r in $x
distinct by $r
return $r;

// Query 2 -- Group By
let $x := [ 
   { "a" : 1, "b" : 1 },
   { "a" : 1, "b" : 1},
   { "a" : 2, "b" : 1},
   { "a" : 1, "b" : 1, "c": 2}
]
for $r in $x
group by $r2 := $r with $r
return $r2;
```

Logical Plan (only relevant portion shown) :

```
//Query 1 -- Distinct
  -- ONE_TO_ONE_EXCHANGE  |LOCAL|
    distinct ([%0->$$1])
    
//Query 2 -- Group By
    group by ([$$4 := %0->$$5]) decor ([]) {
              aggregate [] <- []
              -- AGGREGATE  |UNPARTITIONED|
                nested tuple source
                -- NESTED_TUPLE_SOURCE  |UNPARTITIONED|
           }
```
As you can see, the group by is not rewritten into a distinct.

-- Jules