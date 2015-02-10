## Differences between SQL++ RI and Asterix SQL++

These differences are occured by applying SQL++ on the Asterix Data Model.

#### Datasets

Asterix top-level named values are called datasets.

#### Attributes

SQL++ Data Model Tuples :

```
tupleValue
    : '{' attribute (',' attribute)* '}'
    | '{' '}'
    ;
    
attribute
    : STRING ':' value
    | IDENTIFIER ':' value;
```

Asterix Data Model Tuples (called Records in the Asterix linguo) :

```
RecordConstructor        ::= "{" ( FieldBinding ( "," FieldBinding )* )? "}"
FieldBinding             ::= StringLiteral ":" Expression
```

Notice that an identifier cannot be used as the key of an attribute in the tuple, it **must** be a string. Therefore a TupleValue in the Asterix context cannot be built using an identifier for the name.

#### Breaking down left recursion

While converting the SQL++ RI parser to JavaCC, I have come through the problem of left recursion. JavaCC does not have an automatic way of handling left recursion, therefore the parsing must be broken down a little more carfully. I have found a solution to the problem. It is illustrated in the following example :

```
exprQuery                           // Left recursion
    : exprQuery '.' STRING          # TupleNav
    | exprQuery '.' IDENTIFIER      # TupleNav
    | exprQuery '[' exprQuery ']'   # ArrayNav
    | exprQuery '=' exprQuery       # Eq
    | variable                      # VariableExpr
    | value                         # ValueLiteral
    ;
```

I have solved this problem by applying a left recursion rewriting and creating the  the `RelationshipQuery`, `ValueQuery` and `NavStep` constructs :

```
exprQuery
    : RelationshipQuery ('=' RelationshipQuery)? 	# Eq
    ;

RelationshipQuery
	: ValueQuery (NavStep)*
	;

ValueQuery
	: variable										# VariableExpr
	| value											# ValueLiteral
	;

NavStep
	: '.' IDENTIFIER								#TupleNav
	| '.' STRING									#TupleNav
	| '[' exprQuery ']'								#ArrayNav
	;
```

This rewriting technique seems pretty standard and is what is used by Asterix [to handle their own problem of left recursion](https://asterixdb.ics.uci.edu/documentation/aql/manual.html).

A similar situation breaks down with joins :

```
fromItem                                                           // Left recursion
    : exprQuery AS variable (AT variable)?                         # FromCollectionItem
    | exprQuery AS '{' variable ':' variable '}'                   # FromTupleItem
    | fromItem INNER CORRELATE fromItem                            # FromInnerCorrelateItem
    | fromItem LEFT (OUTER)? CORRELATE fromItem                    # FromLeftCorrelateItem 
    | fromItem FULL (OUTER)? CORRELATE fromItem ON exprQuery       # FromFullCorrelateItem                                               
    ;
```

which we solve as follows :

```
fromItem
	: fromSingle (fromCorrelate)?
	;

fromSingle
	: exprQuery 'AS' fromVariables
	
fromVariables
	: variable (AT variable)?                             # FromCollectionItem
    | '{' variable ':' variable '}'                       # FromTupleItem
    ;
    
fromCorrelate
	: INNER CORRELATE fromItem                            # FromInnerCorrelateItem
    | LEFT (OUTER)? CORRELATE fromItem                    # FromLeftCorrelateItem 
    | FULL (OUTER)? CORRELATE fromItem ON exprQuery       # FromFullCorrelateItem                                               
	;
```

#### Tuple, Bag and Array Values in Select Clause

The current parser description follows these rules to parse tuple, bag and array values.

```
tupleValue
    : '{' attribute (',' attribute)* '}'
    | '{' '}'
    ;
    
attribute
    : STRING ':' value
    | IDENTIFIER ':' value;

arrayValue
    : '[' value (',' value)* ']'
    | '[' ']'
    ;

bagValue
    : '{' '{' value (',' value)* '}' '}'
    | '{' '{' '}' '}'
    ;
```

However with these rules we cannot parse queries such as :

```
from FacebookUsers as fb
select element { "id" : fb.id, "alias" : fb.alias };
```

Therefore the rules were changed to something a little more permissive :

```
tupleValue
    : '{' attribute (',' attribute)* '}'
    | '{' '}'
    ;
    
attribute
    : STRING ':' exprQuery
    | IDENTIFIER ':' exprQuery;

arrayValue
    : '[' exprQuery (',' exprQuery)* ']'
    | '[' ']'
    ;

bagValue
    : '{' '{' exprQuery (',' exprQuery)* '}' '}'
    | '{' '{' '}' '}'
    ;
```

This change of rules also lead to a change in the SQL++ AST, in the Tuple, Array and Bag node classes. List of `Value`s are replaced by List or `ExprQuery`s.

### Queries

#### "Traditional" Select - From - Where

Sample SQL++ query :

```
use dataverse TinySocial;

select $fb.name as name, $fbm
from FacebookUsers as $fb, FacebookMessages as $fbm
where $fb.id = $fbm.author-id and $fb.id = 1;
```

Sample SQL++ query converted to SQL++ core :

```
use dataverse TinySocial;

from FacebookUsers as $fb inner correlate FacebookMessages as $fbm
where $fb.id = $fbm.author-id and $fb.id = 1
select element {"name" : $fb.name as name, "fbm" : $fbm};
```

Equivalent Plan :

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

#### Path Navigation Failures

SQL++ Core query 1:

```
use dataverse TinySocial;

from FacebookUsers as $fb
select element [ "fb" , $fb.employment[0]];
```

Obtained plan :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:ordered-list-constructor, Args:[
    	AString: {fb},
    	function-call: asterix:get-item, Args:[
    		function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {employment}],AInt32: {0}]]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
        empty-tuple-source
```

Output :

```
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
[ "fb", {  } ]
```

SQL++ Core query 2:

```
use dataverse TinySocial;

from FacebookUsers as $fb
select element [ "fb" , $fb.employment[0]];
```

Plan :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:ordered-list-constructor, Args:[
    	AString: {fb},
    	function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {employment}]]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
        empty-tuple-source
```

Output :

```
Internal error. Please check instance logs for further details. [NullPointerException]

```

#### Inner Correlate

Sample SQL++ Core Query :

```
use dataverse TinySocial;

from FacebookUsers as $fb
inner correlate $fb.employment as $emp
select element { "name" : $fb.name, "employment" : $emp };
```

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {employment}, %0->$$1]]
      unnest $$1 <- function-call: asterix:scan-collection, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {employment}]]
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

#### At position

```
no examples yet
```

#### Nested Query

##### From Clause

SQL++ Core Query :

```
use dataverse TinySocial;

from (
	from FacebookUsers as $fb
	select element $fb
) as $fb
select element $fb;
```

...with it's AQL equivalent... :

```
use dataverse TinySocial;

for $fb in (for $fb in dataset FacebookUsers return $fb) return $fb;
```

...and expected plan :

```
distribute result [%0->$$1]
  project ([$$1])
    unnest $$1 <- function-call: asterix:scan-collection, Args:[%0->$$3]
      subplan {
                aggregate [$$3] <- [function-call: asterix:listify, Args:[%0->$$0]]
                  unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
                    nested tuple source
             }
        empty-tuple-source
```

Also tested :

```
use dataverse TinySocial;

from (
	from (
                from FacebookUsers as $fb
                select element $fb
        ) as $fb
	select element $fb
) as $fb
select element $fb;
```

##### Where Clause

SQL++ Core :

```
use dataverse TinySocial;

from FacebookMessages as $fm
where $fm.author-id = (
  select element $fb.id
  from FacebookUsers as $fb
  where $fb.id = 1
)
select element $fm;
```

AQL :

```
use dataverse TinySocial;

for $fm in dataset FacebookMessages
where $fm.author-id = (for $fb in dataset FacebookUsers where $fb.id = 1 return $fb.id)
return $fm;
```

Plan :

```
distribute result [%0->$$0]
  project ([$$0])
    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {author-id}], %0->$$8])
      subplan {
                aggregate [$$8] <- [function-call: asterix:listify, Args:[%0->$$7]]
                  assign [$$7] <- [function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}]]
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}], AInt32: {1}])
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
                        nested tuple source
             }
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
          empty-tuple-source
```

**Warning: Bug Issue**

The above AQL query produce the following wrong output :

```
{ "message-id": 1, "author-id": 3, "in-response-to": 2, "sender-location": point("47.16,77.75"), "message": " love sprint its shortcut-menu is awesome:)" }
{ "message-id": 2, "author-id": 1, "in-response-to": 4, "sender-location": point("41.66,80.87"), "message": " dislike iphone its touch-screen is horrible" }
{ "message-id": 8, "author-id": 1, "in-response-to": 11, "sender-location": point("40.33,80.87"), "message": " like verizon the 3G is awesome:)" }
{ "message-id": 9, "author-id": 3, "in-response-to": 12, "sender-location": point("34.45,96.48"), "message": " love verizon its wireless is good" }
{ "message-id": 10, "author-id": 1, "in-response-to": 12, "sender-location": point("42.5,70.01"), "message": " can't stand motorola the touch-screen is terrible" }
{ "message-id": 13, "author-id": 10, "in-response-to": 4, "sender-location": point("42.77,78.92"), "message": " dislike iphone the voice-command is bad:(" }
{ "message-id": 3, "author-id": 2, "in-response-to": 4, "sender-location": point("48.09,81.01"), "message": " like samsung the plan is amazing" }
{ "message-id": 6, "author-id": 2, "in-response-to": 1, "sender-location": point("31.5,75.56"), "message": " like t-mobile its platform is mind-blowing" }
{ "message-id": 7, "author-id": 5, "in-response-to": 15, "sender-location": point("32.91,85.05"), "message": " dislike sprint the speed is horrible" }
{ "message-id": 12, "author-id": 10, "in-response-to": 6, "sender-location": point("42.26,77.76"), "message": " can't stand t-mobile its voicemail-service is OMG:(" }
{ "message-id": 4, "author-id": 1, "in-response-to": 2, "sender-location": point("37.73,97.04"), "message": " can't stand at&t the network is horrible:(" }
{ "message-id": 5, "author-id": 6, "in-response-to": 2, "sender-location": point("34.7,90.76"), "message": " love sprint the customization is mind-blowing" }
{ "message-id": 11, "author-id": 1, "in-response-to": 1, "sender-location": point("38.97,77.49"), "message": " can't stand at&t its plan is terrible" }
{ "message-id": 14, "author-id": 9, "in-response-to": 12, "sender-location": point("41.33,85.28"), "message": " love at&t its 3G is good:)" }
{ "message-id": 15, "author-id": 7, "in-response-to": 11, "sender-location": point("44.47,67.11"), "message": " like iphone the voicemail-service is awesome" }
```

##### Select Clause

SQL++ Query :

```
use dataverse TinySocial;

from FacebookUsers as $fb
where $fb.id = 1
select element { "name" : $fb.name, "message" : (
	from FacebookMessages as $fm
	where $fm.author-id = $fb.id
	select element $fm.message
)};
```

AQL Query :

```
use dataverse TinySocial;

for $fb in dataset FacebookUsers
return {
"uname": $fb.name,
"messages": for $message in dataset FacebookMessages
       where $message.author-id = $fb.id
       return $message.message
};
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[
    	AString: {uname},
    	function-call: asterix:field-access-by-name, Args:[%0->$$0,AString: {name}],
    	AString: {messages},
    	%0->$$10]]
      subplan {
                aggregate [$$10] <- [function-call: asterix:listify, Args:[%0->$$9]]
                  assign [$$9] <- [function-call: asterix:field-access-by-name, Args:[
                  	%0->$$1,
                  	AString: {message}]]
                    select (function-call: algebricks:eq, Args:[
                    	function-call: asterix:field-access-by-name, Args:[
                    		%0->$$1,
                    		AString: {author-id}],
                    		function-call: asterix:field-access-by-name, Args:[
                    			%0->$$0,
                    			AString: {id}]])
                      unnest $$1 <- function-call: asterix:dataset, Args:[
                      	AString: {FacebookMessages}]
                        nested tuple source
             }
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

### SQL Compatibility


#### Select Clause Rewriting 

SQL++ SQL-style select clause:

```
use dataverse TinySocial;

select $fb.name as "name", $fb.alias as "alias"
from FacebookUsers as $fb;
```

Plan :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {alias}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {alias}]]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
        empty-tuple-source
```

#### From Clause Rewriting


##### Inner Join 

SQL++ Query :

```
use dataverse TinySocial;

select $fb.name as "name", $fm.message as "message"
from FacebookUsers as $fb
join FacebookMessages as $fm
on $fb.id = $fm.author-id;
```

Plan (the subquery is clearly visible):

```
distribute result [%0->$$7]
  project ([$$7])
    assign [$$7] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      unnest $$2 <- function-call: asterix:scan-collection, Args:[%0->$$6]
        subplan {
                  aggregate [$$6] <- [function-call: asterix:listify, Args:[%0->$$1]]
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                        nested tuple source
               }
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

##### Left Outer Join

```
use dataverse TinySocial;

select $fb.name as "name", $fm.message as "message"
from FacebookUsers as $fb
left join FacebookMessages as $fm
on $fb.id = $fm.author-id;
```

Query works but left join not supported.

#### Inner Flatten

SQL++ Query :

```
use dataverse TinySocial;

select $fb.name as "name", $emp as "employment"
from inner flatten (
  FacebookUsers as $fb,
  $fb.employment as $emp
);
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {employment}, %0->$$1]]
      unnest $$1 <- function-call: asterix:scan-collection, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {employment}]]
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

#### Complex constants

##### Array Constant and at

SQL++ Query :

```
use dataverse TinySocial;

select $number as "number", $idx as "idx"
from [3,2,1] as $number at $idx;
```
Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {number}, %0->$$0, AString: {idx}, %0->$$1]]
      unnest $$0 at $$1 <- function-call: asterix:scan-collection, Args:[function-call: asterix:ordered-list-constructor, Args:[AInt32: {3}, AInt32: {2}, AInt32: {1}]]
        empty-tuple-source
```

##### Bag Constant and at

SQL++ Query (note "at" has a random behaviour) :

```
use dataverse TinySocial;

select $number as "number", $idx as "idx"
from {{3,2,1}} as $number at $idx;
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {number}, %0->$$0, AString: {idx}, %0->$$1]]
      unnest $$0 at $$1 <- function-call: asterix:scan-collection, Args:[function-call: asterix:unordered-list-constructor, Args:[AInt32: {3}, AInt32: {2}, AInt32: {1}]]
        empty-tuple-source
```


#### Left Outer Join

SQL++ Query :

```
use dataverse TinySocial;

select $m.message as "message", $u.name as "name"
from FacebookUsers as $u
left join FacebookMessages as $m
on $u.id = $m.author-id;
```

Plan:

```
distribute result [%0->$$5]
  project ([$$5])
    assign [$$5] <- [function-call: asterix:open-record-constructor, Args:[AString: {message}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {message}], AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {name}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {author-id}]])
        left outer join (TRUE)
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
            empty-tuple-source
          unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

Error :

```

java.lang.NullPointerException
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:187)
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:183)
	at edu.uci.ics.hyracks.api.client.impl.JobActivityGraphBuilder.addSourceEdge(JobActivityGraphBuilder.java:77)
	at edu.uci.ics.hyracks.dataflow.std.base.AbstractSingleActivityOperatorDescriptor.contributeActivities(AbstractSingleActivityOperatorDescriptor.java:41)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory$2.visit(JobSpecificationActivityClusterGraphGeneratorFactory.java:63)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visitOperator(PlanUtils.java:37)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visit(PlanUtils.java:30)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory.createActivityClusterGraphGenerator(JobSpecificationActivityClusterGraphGeneratorFactory.java:60)
	at edu.uci.ics.hyracks.control.cc.work.JobStartWork.doRun(JobStartWork.java:57)
	at edu.uci.ics.hyracks.control.common.work.SynchronizableWork.run(SynchronizableWork.java:32)
	at edu.uci.ics.hyracks.control.common.work.WorkQueue$WorkerThread.run(WorkQueue.java:122)
java.lang.NullPointerException
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:187)
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:183)
	at edu.uci.ics.hyracks.api.client.impl.JobActivityGraphBuilder.addSourceEdge(JobActivityGraphBuilder.java:77)
	at edu.uci.ics.hyracks.dataflow.std.base.AbstractSingleActivityOperatorDescriptor.contributeActivities(AbstractSingleActivityOperatorDescriptor.java:41)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory$2.visit(JobSpecificationActivityClusterGraphGeneratorFactory.java:63)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visitOperator(PlanUtils.java:37)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visit(PlanUtils.java:30)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory.createActivityClusterGraphGenerator(JobSpecificationActivityClusterGraphGeneratorFactory.java:60)
	at edu.uci.ics.hyracks.control.cc.work.JobStartWork.doRun(JobStartWork.java:57)
	at edu.uci.ics.hyracks.control.common.work.SynchronizableWork.run(SynchronizableWork.java:32)
	at edu.uci.ics.hyracks.control.common.work.WorkQueue$WorkerThread.run(WorkQueue.java:122)
Feb 03, 2015 10:00:42 AM edu.uci.ics.asterix.api.http.servlet.UIServlet doPost
SEVERE: null
java.lang.NullPointerException
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:187)
	at edu.uci.ics.hyracks.api.job.JobSpecification.getInputConnectorDescriptor(JobSpecification.java:183)
	at edu.uci.ics.hyracks.api.client.impl.JobActivityGraphBuilder.addSourceEdge(JobActivityGraphBuilder.java:77)
	at edu.uci.ics.hyracks.dataflow.std.base.AbstractSingleActivityOperatorDescriptor.contributeActivities(AbstractSingleActivityOperatorDescriptor.java:41)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory$2.visit(JobSpecificationActivityClusterGraphGeneratorFactory.java:63)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visitOperator(PlanUtils.java:37)
	at edu.uci.ics.hyracks.api.client.impl.PlanUtils.visit(PlanUtils.java:30)
	at edu.uci.ics.hyracks.api.client.impl.JobSpecificationActivityClusterGraphGeneratorFactory.createActivityClusterGraphGenerator(JobSpecificationActivityClusterGraphGeneratorFactory.java:60)
	at edu.uci.ics.hyracks.control.cc.work.JobStartWork.doRun(JobStartWork.java:57)
	at edu.uci.ics.hyracks.control.common.work.SynchronizableWork.run(SynchronizableWork.java:32)
	at edu.uci.ics.hyracks.control.common.work.WorkQueue$WorkerThread.run(WorkQueue.java:122)
```

#### Syntax Differences

 - We use the `$` to identify variables (difference with SQL++ core).
 - The SQL style select clause aliases are required to be surrounded by quotes (`""`).

The syntax changes make it easy to identify which elements are variables and which elements are top-level named values (a.k.a datasets). The absence of identifers means that a metadata lookup is required to figure out if a named value is a dataset or a variable. SQL++ RI does not have this distinction.

What should we do? N1QL may provide a source of inspiration.



### Unimplemented clauses 

 - select attribute **impossible**
 - from left correlate **medium**
 - from full correlate **impossible**
 - from A as { k : v } **impossible**
 - operator expressions **easy** (not a priority)
 - from at **done**
 - nesting **done**
 - group by **impossible**
 - ast rewritings **done**
 - complex constants **done**
 - ExprQuery as root clause **easy** (not a priority)
 
## What's missing?
 - ExprQuery as root clause [2h]
 - Complex constant expressions [2h]
 - Operation expressions (AND, OR, +, -, <, <=...) : only EQ exists [2h]
 - Group By, Having 
 - Order By, Limit, Offset 
 - select attribute
 - from left correlate
 - from full correlate
 - from inner correlate with correlated var in right clause [2h]
 - existensial quantifiers (IN, EXISTS...)