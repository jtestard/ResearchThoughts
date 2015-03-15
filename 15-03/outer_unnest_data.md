Query :

```
use dataverse TinySocial;

select user.name as user, message as message
from FacebookUsers as user
join FacebookMessages as message
on user.id = message.author-id;
```

Logical Plan :

```
distribute result [%0->$$8] -- |UNPARTITIONED|
  project ([$$8]) -- |UNPARTITIONED|
    assign [$$8] <- [function-call: asterix:open-record-constructor, Args:[AString: {user}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {message}, %0->$$2]] -- |UNPARTITIONED|
      unnest $$2 <- function-call: asterix:scan-collection, Args:[%0->$$7] -- |UNPARTITIONED|
        subplan {
                  aggregate [$$7] <- [function-call: asterix:listify, Args:[%0->$$1]] -- |UNPARTITIONED|
                    select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]]) -- |UNPARTITIONED|
                      unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}] -- |UNPARTITIONED|
                        nested tuple source -- |UNPARTITIONED|
               } -- |UNPARTITIONED|
          unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] -- |UNPARTITIONED|
            empty-tuple-source -- |UNPARTITIONED|
```

Optimized Logical Plan :

```
distribute result [%0->$$8]
-- DISTRIBUTE_RESULT  |PARTITIONED|
  exchange 
  -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
    project ([$$8])
    -- STREAM_PROJECT  |PARTITIONED|
      assign [$$8] <- [function-call: asterix:closed-record-constructor, Args:[AString: {user}, %0->$$16, AString: {message}, %0->$$1]]
      -- ASSIGN  |PARTITIONED|
        project ([$$1, $$16])
        -- STREAM_PROJECT  |PARTITIONED|
          exchange 
          -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
            join (function-call: algebricks:eq, Args:[%0->$$13, %0->$$15])
            -- HYBRID_HASH_JOIN [$$13][$$15]  |PARTITIONED|
              exchange 
              -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                project ([$$16, $$13])
                -- STREAM_PROJECT  |PARTITIONED|
                  assign [$$16] <- [function-call: asterix:field-access-by-index, Args:[%0->$$0, AInt32: {2}]]
                  -- ASSIGN  |PARTITIONED|
                    exchange 
                    -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                      data-scan []<-[$$13, $$0] <- TinySocial:FacebookUsers
                      -- DATASOURCE_SCAN  |PARTITIONED|
                        exchange 
                        -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                          empty-tuple-source
                          -- EMPTY_TUPLE_SOURCE  |PARTITIONED|
              exchange 
              -- HASH_PARTITION_EXCHANGE [$$15]  |PARTITIONED|
                assign [$$15] <- [function-call: asterix:field-access-by-index, Args:[%0->$$1, AInt32: {1}]]
                -- ASSIGN  |PARTITIONED|
                  project ([$$1])
                  -- STREAM_PROJECT  |PARTITIONED|
                    exchange 
                    -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                      data-scan []<-[$$11, $$1] <- TinySocial:FacebookMessages
                      -- DATASOURCE_SCAN  |PARTITIONED|
                        exchange 
                        -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                          empty-tuple-source
                          -- EMPTY_TUPLE_SOURCE  |PARTITIONED|
```

Hyracks Job Specification :

```
{
 "connectors": [
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:0]",
    "id": "CDID:0",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:8",
   "in-operator-port": 0,
   "out-operator-id": "ODID:0",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:1]",
    "id": "CDID:1",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:0",
   "in-operator-port": 0,
   "out-operator-id": "ODID:6",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:2]",
    "id": "CDID:2",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:6",
   "in-operator-port": 0,
   "out-operator-id": "ODID:2",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:3]",
    "id": "CDID:3",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:4",
   "in-operator-port": 0,
   "out-operator-id": "ODID:1",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:4]",
    "id": "CDID:4",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:1",
   "in-operator-port": 0,
   "out-operator-id": "ODID:7",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.MToNPartitioningConnectorDescriptor[CDID:5]",
    "id": "CDID:5",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.MToNPartitioningConnectorDescriptor"
   },
   "in-operator-id": "ODID:7",
   "in-operator-port": 0,
   "out-operator-id": "ODID:2",
   "out-operator-port": 1
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:6]",
    "id": "CDID:6",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:2",
   "in-operator-port": 0,
   "out-operator-id": "ODID:5",
   "out-operator-port": 0
  },
  {
   "connector": {
    "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:7]",
    "id": "CDID:7",
    "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
   },
   "in-operator-id": "ODID:5",
   "in-operator-port": 0,
   "out-operator-id": "ODID:3",
   "out-operator-port": 0
  }
 ],
 "operators": [
  {
   "display-name": "edu.uci.ics.hyracks.storage.am.btree.dataflow.BTreeSearchOperatorDescriptor[ODID:0]",
   "id": "ODID:0",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.storage.am.btree.dataflow.BTreeSearchOperatorDescriptor",
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.storage.am.btree.dataflow.BTreeSearchOperatorDescriptor[ODID:1]",
   "id": "ODID:1",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.storage.am.btree.dataflow.BTreeSearchOperatorDescriptor",
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.dataflow.std.join.OptimizedHybridHashJoinOperatorDescriptor[ODID:2]",
   "id": "ODID:2",
   "in-arity": 2,
   "java-class": "edu.uci.ics.hyracks.dataflow.std.join.OptimizedHybridHashJoinOperatorDescriptor",
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor[ODID:3]",
   "id": "ODID:3",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor",
   "out-arity": 0,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:4]",
   "id": "ODID:4",
   "in-arity": 0,
   "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
   "micro-operators": ["ets"],
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:5]",
   "id": "ODID:5",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
   "micro-operators": [
    "stream-project [2, 0]",
    "assign [2] := [edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$ScalarEvaluatorFactoryAdapter@5b33e8d6]",
    "stream-project [2]"
   ],
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:6]",
   "id": "ODID:6",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
   "micro-operators": [
    "assign [2] := [edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$ScalarEvaluatorFactoryAdapter@2cfb6861]",
    "stream-project [2, 0]"
   ],
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:7]",
   "id": "ODID:7",
   "in-arity": 1,
   "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
   "micro-operators": [
    "stream-project [1]",
    "assign [1] := [edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$ScalarEvaluatorFactoryAdapter@2d81cf59]"
   ],
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  },
  {
   "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:8]",
   "id": "ODID:8",
   "in-arity": 0,
   "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
   "micro-operators": ["ets"],
   "out-arity": 1,
   "partition-constraints": {
    "count": "4",
    "location": {
     "0": "nc1",
     "1": "nc1",
     "2": "nc2",
     "3": "nc2"
    }
   }
  }
 ]
}
[PARTITION_LOCATION(ODID:7, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:3, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:7, 1) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:8, 2) in CONSTANT[nc2:java.lang.String], PARTITION_COUNT(ODID:3) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:5, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:8, 1) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:1) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:4, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:3, 1) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:1, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:4, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:1, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:4, 1) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:0) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:2, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:0, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:7, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:6, 1) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:4) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:2, 1) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:2) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:1, 1) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:5, 2) in CONSTANT[nc2:java.lang.String], PARTITION_COUNT(ODID:5) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:8, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:5, 0) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:8) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:4, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:0, 0) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:6) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:3, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:8, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:5, 1) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:7, 0) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:6, 0) in CONSTANT[nc1:java.lang.String], PARTITION_COUNT(ODID:7) in CONSTANT[4:java.lang.Integer], PARTITION_LOCATION(ODID:0, 1) in CONSTANT[nc1:java.lang.String], PARTITION_LOCATION(ODID:2, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:6, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:3, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:2, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:1, 2) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:6, 3) in CONSTANT[nc2:java.lang.String], PARTITION_LOCATION(ODID:0, 3) in CONSTANT[nc2:java.lang.String]]
```