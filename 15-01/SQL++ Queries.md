#SQL++ Queries


### Query 0 Exact Match Lookup

##### a. Using SQL++ Core

Query :

```
use dataverse TinySocial;

from FacebookUsers as fb
where fb.id = 8
select element { "user" : fb};
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {user}, %0->$$0]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {8}])
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

Output :

```
{ "user": { "id": 8, "alias": "Nila", "name": "NilaMilliron", "user-since": datetime("2008-01-01T10:10:00.000Z"), "friend-ids": {{ 3 }}, "employment": [ { "organization-name": "Plexlane", "start-date": date("2010-02-28"), "end-date": null } ] } }
```

##### b. Using SQL++ SQL-style

Query :

```
use dataverse TinySocial;

select fb as "user"
from FacebookUsers as fb
where fb.id = 8;
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {user}, %0->$$0]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {8}])
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
          empty-tuple-source
```

Output :

```
{ "user": { "id": 8, "alias": "Nila", "name": "NilaMilliron", "user-since": datetime("2008-01-01T10:10:00.000Z"), "friend-ids": {{ 3 }}, "employment": [ { "organization-name": "Plexlane", "start-date": date("2010-02-28"), "end-date": null } ] } }
```

### Query 1 Equi-Join

##### a. Using SQL++ Core

Query :

```
use dataverse TinySocial;

from FacebookUsers as fb inner correlate FacebookMessages as fbm
where fb.id = fbm.author-id
select element {"name" : fb.name, "message" : fbm.message};
```

Plan :

```
distribute result [%0->$$5]
  project ([$$5])
    assign [$$5] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
        unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

Output :

```
{ "name": "MargaritaStoddard", "message": " dislike iphone its touch-screen is horrible" }
{ "name": "MargaritaStoddard", "message": " like verizon the 3G is awesome:)" }
{ "name": "MargaritaStoddard", "message": " can't stand motorola the touch-screen is terrible" }
{ "name": "MargaritaStoddard", "message": " can't stand at&t the network is horrible:(" }
{ "name": "MargaritaStoddard", "message": " can't stand at&t its plan is terrible" }
{ "name": "IsbelDull", "message": " like samsung the plan is amazing" }
{ "name": "IsbelDull", "message": " like t-mobile its platform is mind-blowing" }
{ "name": "WoodrowNehling", "message": " love at&t its 3G is good:)" }
{ "name": "BramHatch", "message": " dislike iphone the voice-command is bad:(" }
{ "name": "BramHatch", "message": " can't stand t-mobile its voicemail-service is OMG:(" }
{ "name": "EmoryUnk", "message": " love sprint its shortcut-menu is awesome:)" }
{ "name": "EmoryUnk", "message": " love verizon its wireless is good" }
{ "name": "WillisWynne", "message": " love sprint the customization is mind-blowing" }
{ "name": "SuzannaTillson", "message": " like iphone the voicemail-service is awesome" }
{ "name": "VonKemble", "message": " dislike sprint the speed is horrible" }
```

##### b. Using SQL++ SQL-style

Query :

```
use dataverse TinySocial;

select fb.name as "name", fbm.message as "message"
from FacebookUsers as fb , FacebookMessages as fbm
where fb.id = fbm.author-id;
```

Plan :

```
distribute result [%0->$$5]
  project ([$$5])
    assign [$$5] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
        unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

Output :

```
{ "name": "MargaritaStoddard", "message": " dislike iphone its touch-screen is horrible" }
{ "name": "MargaritaStoddard", "message": " like verizon the 3G is awesome:)" }
{ "name": "MargaritaStoddard", "message": " can't stand motorola the touch-screen is terrible" }
{ "name": "MargaritaStoddard", "message": " can't stand at&t the network is horrible:(" }
{ "name": "MargaritaStoddard", "message": " can't stand at&t its plan is terrible" }
{ "name": "IsbelDull", "message": " like samsung the plan is amazing" }
{ "name": "IsbelDull", "message": " like t-mobile its platform is mind-blowing" }
{ "name": "WoodrowNehling", "message": " love at&t its 3G is good:)" }
{ "name": "BramHatch", "message": " dislike iphone the voice-command is bad:(" }
{ "name": "BramHatch", "message": " can't stand t-mobile its voicemail-service is OMG:(" }
{ "name": "EmoryUnk", "message": " love sprint its shortcut-menu is awesome:)" }
{ "name": "EmoryUnk", "message": " love verizon its wireless is good" }
{ "name": "WillisWynne", "message": " love sprint the customization is mind-blowing" }
{ "name": "SuzannaTillson", "message": " like iphone the voicemail-service is awesome" }
{ "name": "VonKemble", "message": " dislike sprint the speed is horrible" }
```

### Query 2 Nested Query

##### a. From Clause

Query (uses nesting induced by AST rewriting) :

```
use dataverse TinySocial;

select fb.name as "name", fbm.message as "message"
from FacebookUsers as fb left join FacebookMessages as fbm
on fb.id = fbm.author-id;
```

AST :

```
{
  "Query":[
    {
      "from":{
        "left collection":{
          "collection":"FacebookUsers[-1][dataset]",
          "as":"fb[0]"
        },
        "left correlate right item":{
          "collection":{
            "nested":[
              {
                "from":{
                  "collection":"FacebookMessages[-1][dataset]",
                  "as":"fbm[1]"
                }
              },
              {
                "where":{
                  "function":"eq",
                  "arguments":[
                    {
                      "function":"tuple_nav",
                      "arguments":[
                        "fb[0]",
                        "id"
                      ]
                    },
                    {
                      "function":"tuple_nav",
                      "arguments":[
                        "fbm[1]",
                        "author-id"
                      ]
                    }
                  ]
                }
              },
              {
                "select element":"fbm[1]"
              }
            ]
          },
          "as":"fbm[2]"
        }
      }
    },
    {
      "select element":{
        "name":{
          "function":"tuple_nav",
          "arguments":[
            "fb[0]",
            "name"
          ]
        },
        "message":{
          "function":"tuple_nav",
          "arguments":[
            "fbm[1]",
            "message"
          ]
        }
      }
    }
  ]
}
```

The `listify` function in Asterix returns a single tuple with an empty list when its source is empty (all incoming tuples filtered out). Because of the semantics of `listify`, the following plan will give a correct output.

Plan :

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

Output :

```
{ "name": "MargaritaStoddard", "message": " can't stand at&t the network is horrible:(" }
{ "name": "MargaritaStoddard", "message": " can't stand at&t its plan is terrible" }
{ "name": "MargaritaStoddard", "message": " dislike iphone its touch-screen is horrible" }
{ "name": "MargaritaStoddard", "message": " like verizon the 3G is awesome:)" }
{ "name": "MargaritaStoddard", "message": " can't stand motorola the touch-screen is terrible" }
{ "name": "IsbelDull", "message": " like samsung the plan is amazing" }
{ "name": "IsbelDull", "message": " like t-mobile its platform is mind-blowing" }
{ "name": "EmoryUnk", "message": " love sprint its shortcut-menu is awesome:)" }
{ "name": "EmoryUnk", "message": " love verizon its wireless is good" }
{ "name": "NicholasStroh", "message": null }
{ "name": "VonKemble", "message": " dislike sprint the speed is horrible" }
{ "name": "WillisWynne", "message": " love sprint the customization is mind-blowing" }
{ "name": "SuzannaTillson", "message": " like iphone the voicemail-service is awesome" }
{ "name": "NilaMilliron", "message": null }
{ "name": "WoodrowNehling", "message": " love at&t its 3G is good:)" }
{ "name": "BramHatch", "message": " can't stand t-mobile its voicemail-service is OMG:(" }
{ "name": "BramHatch", "message": " dislike iphone the voice-command is bad:(" }
```

##### b. Where Clause

Query : 

```
use dataverse TinySocial;

from FacebookMessages as fm
where fm.author-id = (
  select element fb.id
  from FacebookUsers as fb
  where fb.id = 1
)
select element fm;
```
Plan :

```
distribute result [%0->$$0]
  project ([$$0])
    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {author-id}], %0->$$6])
      subplan {
                aggregate [$$6] <- [function-call: asterix:listify, Args:[%0->$$5]]
                  assign [$$5] <- [function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}]]
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {id}], AInt32: {1}])
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
                        nested tuple source
             }
        unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
          empty-tuple-source
```

Output :

```
{ "message-id": 2, "author-id": 1, "in-response-to": 4, "sender-location": point("41.66,80.87"), "message": " dislike iphone its touch-screen is horrible" }
{ "message-id": 8, "author-id": 1, "in-response-to": 11, "sender-location": point("40.33,80.87"), "message": " like verizon the 3G is awesome:)" }
{ "message-id": 10, "author-id": 1, "in-response-to": 12, "sender-location": point("42.5,70.01"), "message": " can't stand motorola the touch-screen is terrible" }
{ "message-id": 13, "author-id": 10, "in-response-to": 4, "sender-location": point("42.77,78.92"), "message": " dislike iphone the voice-command is bad:(" }
{ "message-id": 3, "author-id": 2, "in-response-to": 4, "sender-location": point("48.09,81.01"), "message": " like samsung the plan is amazing" }
{ "message-id": 6, "author-id": 2, "in-response-to": 1, "sender-location": point("31.5,75.56"), "message": " like t-mobile its platform is mind-blowing" }
{ "message-id": 12, "author-id": 10, "in-response-to": 6, "sender-location": point("42.26,77.76"), "message": " can't stand t-mobile its voicemail-service is OMG:(" }
{ "message-id": 4, "author-id": 1, "in-response-to": 2, "sender-location": point("37.73,97.04"), "message": " can't stand at&t the network is horrible:(" }
{ "message-id": 11, "author-id": 1, "in-response-to": 1, "sender-location": point("38.97,77.49"), "message": " can't stand at&t its plan is terrible" }
{ "message-id": 14, "author-id": 9, "in-response-to": 12, "sender-location": point("41.33,85.28"), "message": " love at&t its 3G is good:)" }
{ "message-id": 1, "author-id": 3, "in-response-to": 2, "sender-location": point("47.16,77.75"), "message": " love sprint its shortcut-menu is awesome:)" }
{ "message-id": 9, "author-id": 3, "in-response-to": 12, "sender-location": point("34.45,96.48"), "message": " love verizon its wireless is good" }
{ "message-id": 5, "author-id": 6, "in-response-to": 2, "sender-location": point("34.7,90.76"), "message": " love sprint the customization is mind-blowing" }
{ "message-id": 15, "author-id": 7, "in-response-to": 11, "sender-location": point("44.47,67.11"), "message": " like iphone the voicemail-service is awesome" }
{ "message-id": 7, "author-id": 5, "in-response-to": 15, "sender-location": point("32.91,85.05"), "message": " dislike sprint the speed is horrible" }
```

###### Bug report (subqueries in where clause don't work in neither AQL nor SQL++)

##### c. Select Clause

Query : 

```
use dataverse TinySocial;

from FacebookUsers as fb
where fb.id = 1
select element { "name" : fb.name, "message" : (
    from FacebookMessages as fm
    where fm.author-id = fb.id
    select element fm.message
)};
```

Plan :

```
distribute result [%0->$$4]
  project ([$$4])
    assign [$$4] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, %0->$$10]]
      subplan {
                aggregate [$$10] <- [function-call: asterix:listify, Args:[%0->$$9]]
                  assign [$$9] <- [function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}], function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}]])
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                        nested tuple source
             }
        select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {1}])
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
```

Output :

```
{ "name": "MargaritaStoddard", "message": [ " dislike iphone its touch-screen is horrible", " like verizon the 3G is awesome:)", " can't stand motorola the touch-screen is terrible", " can't stand at&t the network is horrible:(", " can't stand at&t its plan is terrible" ] }
```

### Query 3 Inner Flatten

Query :

```
use dataverse TinySocial;

select fb.name as name, emp as employment
from inner flatten (
  dataset FacebookUsers as fb,
  fb.employment as emp
);
```

AST : 

```
{
  "Query":[
    {
      "from":{
        "left collection":{
          "collection":"FacebookUsers[-1][dataset]",
          "as":"fb[0]"
        },
        "inner correlate right item":{
          "collection":{
            "function":"tuple_nav",
            "arguments":[
              "fb[0]",
              "employment"
            ]
          },
          "as":"$emp[1]"
        }
      }
    },
    {
      "select element":{
        "name":{
          "function":"tuple_nav",
          "arguments":[
            "fb[0]",
            "name"
          ]
        },
        "employment":"$emp[1]"
      }
    }
  ]
}
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

Output :

```
{ "name": "MargaritaStoddard", "employment": { "organization-name": "Codetechno", "start-date": date("2006-08-06"), "end-date": null } }
{ "name": "IsbelDull", "employment": { "organization-name": "Hexviafind", "start-date": date("2010-04-27"), "end-date": null } }
{ "name": "NilaMilliron", "employment": { "organization-name": "Plexlane", "start-date": date("2010-02-28"), "end-date": null } }
{ "name": "WoodrowNehling", "employment": { "organization-name": "Zuncan", "start-date": date("2003-04-22"), "end-date": date("2009-12-13") } }
{ "name": "BramHatch", "employment": { "organization-name": "physcane", "start-date": date("2007-06-05"), "end-date": date("2011-11-05") } }
{ "name": "EmoryUnk", "employment": { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } }
{ "name": "WillisWynne", "employment": { "organization-name": "jaydax", "start-date": date("2009-05-15"), "end-date": null } }
{ "name": "SuzannaTillson", "employment": { "organization-name": "Labzatron", "start-date": date("2011-04-19"), "end-date": null } }
{ "name": "NicholasStroh", "employment": { "organization-name": "Zamcorporation", "start-date": date("2010-06-08"), "end-date": null } }
{ "name": "VonKemble", "employment": { "organization-name": "Kongreen", "start-date": date("2010-11-27"), "end-date": null } }
```

### Query 4 Non-tuple output

Query : 

```
use dataverse TinySocial;

from FacebookUsers as u
select element [ u.name, u.alias ];
```

Plan :

```
distribute result [%0->$$1]
  project ([$$1])
    assign [$$1] <- [function-call: asterix:ordered-list-constructor, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {alias}]]]
      unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
        empty-tuple-source
```

Output :

```
[ "MargaritaStoddard", "Margarita" ]
[ "IsbelDull", "Isbel" ]
[ "NilaMilliron", "Nila" ]
[ "WoodrowNehling", "Woodrow" ]
[ "BramHatch", "Bram" ]
[ "EmoryUnk", "Emory" ]
[ "WillisWynne", "Willis" ]
[ "SuzannaTillson", "Suzanna" ]
[ "NicholasStroh", "Nicholas" ]
[ "VonKemble", "Von" ]
```

### Query 5 Complex Constants


Query : 

```
use dataverse TinySocial;

select v as v, i as i
from [3, 2, 1] as v at i;
```

Plan :

```
distribute result [%0->$$3]
  project ([$$3])
    assign [$$3] <- [function-call: asterix:open-record-constructor, Args:[AString: {v}, %0->$$0, AString: {i}, %0->$$1]]
      unnest $$0 at $$1 <- function-call: asterix:scan-collection, Args:[function-call: asterix:ordered-list-constructor, Args:[AInt32: {3}, AInt32: {2}, AInt32: {1}]]
        empty-tuple-source
```

Output :

```
{ "v": 3, "i": 1 }
{ "v": 2, "i": 2 }
{ "v": 1, "i": 3 }
```

### Query 6

Variable tests :

```
```

### Query 7 : Bypassing core rewriting

Take the following extended SQL++ query :

```
use dataverse TinySocial;

select fb.name as name, fbm.message
from dataset FacebookUsers as fb
join dataset FacebookMessages as fbm
on fb.id = fbm.author-id
where fb.id = 1;
```

Core Plan :

```
distribute result [%0->$$11]
  project ([$$11])
    assign [$$11] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {fbm}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {1}])
        unnest $$2 <- function-call: asterix:scan-collection, Args:[%0->$$8]
          subplan {
                    aggregate [$$8] <- [function-call: asterix:listify, Args:[%0->$$1]]
                      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
                        unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                          nested tuple source
                 }
            unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
              empty-tuple-source
```

Extended Plan :

```
distribute result [%0->$$9]
  project ([$$9])
    assign [$$9] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {fbm}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {1}])
        select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
          unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
            unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
              empty-tuple-source
```