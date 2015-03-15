## Plan translation Milestone 1

We currently try to support SQL++ translation for queries which do not have any of the following :

 - Position variables.
 - Nested Subqueries.
 - Group By queries.
 - Set operators.
 - Syntactic sugar.
 - Flatten operator.
 - Function calls (other than operators from OperatorExpression)
 - Quantified expressions `IN, EXISTS`..


## Query 1

Sample SQL++ query :

```
use dataverse TinySocial;

select fb
from FacebookUsers as fb;
```

Equivalent Plan :

```
distribute result [%0->$$0] 
  project ([$$0]) 
    unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] 
      empty-tuple-source 
```

## Query 2

Introduce tuple navigation.

	use dataverse TinySocial;
	
	select fb.id
	from FacebookUsers as fb;
	

## Query 3

Multiple elements in select clause 

	use dataverse TinySocial;
	
	select fb.id, fb.alias
	from FacebookUsers as fb
	
Equivalent Plan :

	distribute result [%0->$$2] 
  		project ([$$2]) 
    		assign [$$2] <- [function-call: asterix:open-record-constructor, Args:[
    			AString: {id}, 
    			function-call: 
    				asterix:field-access-by-name, 
    				Args:[%0->$$0, AString: {id}],
    			AString: {alias},
    			function-call:
    				asterix:field-access-by-name,
    				Args:[%0->$$0, AString: {alias}]]] 
      		unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] 
        	empty-tuple-source 

## Query 4

Multiple items in from clause

```
use dataverse TinySocial;

select fb1.id, fib2.id
from FacebookUsers as fb1, FacebookUsers as fb2;
```

Obtained plan :

```
distribute result [%0->$$4] 
  project ([$$4]) 
    assign [$$4] <- [function-call: asterix:open-record-constructor, Args:[
    	AString: {fb1},
    	function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}],
    	AString: {fb2},
    	function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}]]] 
      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] 
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] 
          empty-tuple-source 
```

## Query 5

```
use dataverse TinySocial;

select fb1.id, fb2.name
from FacebookUsers as fb1, FacebookUsers as fb2
where fb1.id = fb2.id ;
```

obtained plan :

```
distribute result [%0->$$7]
  project ([$$7])
    assign [$$7] <- [function-call: asterix:open-record-constructor, Args:[
    AString: {fb1},
    function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}],
    AString: {fb2},
    function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}]]]
      select (function-call: algebricks:eq, Args:[
      function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}],
      function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}]])
        unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

Missing features :

 - Unsupported operations.
 - Vague error messages (error should be detected sooner).
 
## Query 6

```
use dataverse TinySocial;

select fb.name as name, fbm
from FacebookUsers as fb, FacebookMessages as fbm
where fb.id = fbm.author-id and fb.id = 1;
```

obtained plan :

```
distribute result [%0->$$7]
  project ([$$7])
    assign [$$7] <- [function-call: asterix:open-record-constructor, Args:[
    AString: {name},
    function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}],
    AString: {fbm},
    %0->$$2
    ]]
      select (
      	function-call: algebricks:and, Args:[
      		function-call: algebricks:eq, Args:[
      			function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}],
      			function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {author-id}]],
      		function-call: algebricks:eq, Args:[
      			function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}],
      			AInt32: {1}
      			]
      		])
        unnest $$2 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

## Query 7

query :

```
use dataverse TinySocial;

select twm.user.screen-name
from TweetMessages as twm;
```

plan obtained :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:open-record-constructor, Args:[AString: {twm.user.screen-name}, function-call: asterix:field-access-by-name, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {user}], AString: {screen-name}]]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {TweetMessages}]
        empty-tuple-source
```

## Query 8 
Array navigation

```
use dataverse TinySocial;

select fb.name as name, fb.employment[0] as employment
from FacebookUsers as fb;
```

plan :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:open-record-constructor, Args:[
    	AString: {name},
    	function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}],
    	AString: {employment},
    	function-call: asterix:get-item, Args:[
    		function-call: asterix:field-access-by-name, Args:[
    			%0->$$0,
    			AString: {employment}
    		],
    		AInt32: {0}]
    	]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
        empty-tuple-source
```

### Notes

 - What are broadcast operands?
 - What are hint annotations?
 - Missing is not handled.