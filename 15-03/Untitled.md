Logical Plan : 

```
distribute result [%0->$$8]
  project ([$$8])
    assign [$$8] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, %0->$$2]]
      unnest $$2 <- function-call: asterix:scan-collection, Args:[%0->$$7]
        subplan {
                  aggregate [$$7] <- [function-call: asterix:listify, Args:[%0->$$1]]
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                        nested tuple source
               }
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
            empty-tuple-source
Optimized logical plan:
```

Optimized Plan :

```
distribute result [%0->$$8]
-- DISTRIBUTE_RESULT
  exchange 
  -- ONE_TO_ONE_EXCHANGE
    project ([$$8])
    -- STREAM_PROJECT
      assign [$$8] <- [function-call: asterix:closed-record-constructor, Args:[AString: {name}, %0->$$16, AString: {message}, %0->$$1]]
      -- ASSIGN
        project ([$$1, $$16])
        -- STREAM_PROJECT
          exchange 
          -- ONE_TO_ONE_EXCHANGE
            join (function-call: algebricks:eq, Args:[%0->$$13, %0->$$15])
            -- HYBRID_HASH_JOIN [$$13][$$15]
              exchange 
              -- ONE_TO_ONE_EXCHANGE
                project ([$$16, $$13])
                -- STREAM_PROJECT
                  assign [$$16] <- [function-call: asterix:field-access-by-index, Args:[%0->$$0, AInt32: {2}]]
                  -- ASSIGN
                    exchange 
                    -- ONE_TO_ONE_EXCHANGE
                      data-scan []<-[$$13, $$0] <- TinySocial:FacebookUsers
                      -- DATASOURCE_SCAN
                        exchange 
                        -- ONE_TO_ONE_EXCHANGE
                          empty-tuple-source
                          -- EMPTY_TUPLE_SOURCE
              exchange 
              -- HASH_PARTITION_EXCHANGE [$$15]
                assign [$$15] <- [function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {1}]]
                -- ASSIGN
                  project ([$$1])
                  -- STREAM_PROJECT
                    exchange 
                    -- ONE_TO_ONE_EXCHANGE
                      data-scan []<-[$$11, $$1] <- TinySocial:FacebookMessages
                      -- DATASOURCE_SCAN
                        exchange 
                        -- ONE_TO_ONE_EXCHANGE
                          empty-tuple-source
                          -- EMPTY_TUPLE_SOURCE
```

Results:

```
{ "name": "MargaritaStoddard", "message": { "message-id": 2, "author-id": 1, "in-response-to": 4, "sender-location": point("41.66,80.87"), "message": " dislike iphone its touch-screen is horrible" } }
{ "name": "MargaritaStoddard", "message": { "message-id": 8, "author-id": 1, "in-response-to": 11, "sender-location": point("40.33,80.87"), "message": " like verizon the 3G is awesome:)" } }
{ "name": "MargaritaStoddard", "message": { "message-id": 10, "author-id": 1, "in-response-to": 12, "sender-location": point("42.5,70.01"), "message": " can't stand motorola the touch-screen is terrible" } }
{ "name": "MargaritaStoddard", "message": { "message-id": 4, "author-id": 1, "in-response-to": 2, "sender-location": point("37.73,97.04"), "message": " can't stand at&t the network is horrible:(" } }
{ "name": "MargaritaStoddard", "message": { "message-id": 11, "author-id": 1, "in-response-to": 1, "sender-location": point("38.97,77.49"), "message": " can't stand at&t its plan is terrible" } }
{ "name": "IsbelDull", "message": { "message-id": 3, "author-id": 2, "in-response-to": 4, "sender-location": point("48.09,81.01"), "message": " like samsung the plan is amazing" } }
{ "name": "IsbelDull", "message": { "message-id": 6, "author-id": 2, "in-response-to": 1, "sender-location": point("31.5,75.56"), "message": " like t-mobile its platform is mind-blowing" } }
{ "name": "WoodrowNehling", "message": { "message-id": 14, "author-id": 9, "in-response-to": 12, "sender-location": point("41.33,85.28"), "message": " love at&t its 3G is good:)" } }
{ "name": "BramHatch", "message": { "message-id": 13, "author-id": 10, "in-response-to": 4, "sender-location": point("42.77,78.92"), "message": " dislike iphone the voice-command is bad:(" } }
{ "name": "BramHatch", "message": { "message-id": 12, "author-id": 10, "in-response-to": 6, "sender-location": point("42.26,77.76"), "message": " can't stand t-mobile its voicemail-service is OMG:(" } }
{ "name": "EmoryUnk", "message": { "message-id": 1, "author-id": 3, "in-response-to": 2, "sender-location": point("47.16,77.75"), "message": " love sprint its shortcut-menu is awesome:)" } }
{ "name": "EmoryUnk", "message": { "message-id": 9, "author-id": 3, "in-response-to": 12, "sender-location": point("34.45,96.48"), "message": " love verizon its wireless is good" } }
{ "name": "WillisWynne", "message": { "message-id": 5, "author-id": 6, "in-response-to": 2, "sender-location": point("34.7,90.76"), "message": " love sprint the customization is mind-blowing" } }
{ "name": "SuzannaTillson", "message": { "message-id": 15, "author-id": 7, "in-response-to": 11, "sender-location": point("44.47,67.11"), "message": " like iphone the voicemail-service is awesome" } }
{ "name": "VonKemble", "message": { "message-id": 7, "author-id": 5, "in-response-to": 15, "sender-location": point("32.91,85.05"), "message": " dislike sprint the speed is horrible" } }
Duration of all jobs: 11.131 sec
Success: Query Complete
```