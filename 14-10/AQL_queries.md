## AQL query language

### 1. Important Commands

	managix create -n my_asterix
	managix start -n my_asterix
	managix stop -n my_asterix

### 2. Example Queries

The evaluation of the following queries has been done on a single node environment with no partitioning. This is apparent in the Hyracks specifications obtained.

NOTE : Output is stored in register `%0`, as can be seen in logical plans. Variables are denoted as `$$x`, where `x` is their id. 

#### 2.1 Hello World
**Input**: 

	let $message := 'Hello World!'
    return $message

**Output**:

	"Hello World"

**Rewritten Expression**:

    Query:
    FLWOGR [
      Let Variable [ Name=$message Id=0 ]
        :=  
        LiteralExpr [STRING] [Hello World!] 
      Return
        Variable [ Name=$message Id=0 ]
    ]

**Logical Plan**:

	distribute result [%0->$$0] -- |UNPARTITIONED|
	  project ([$$0]) -- |UNPARTITIONED|
    	assign [$$0] <- [AString: {Hello World!}] -- |UNPARTITIONED|
	      empty-tuple-source -- |UNPARTITIONED|

**Hyracks Job Specification**:

    {
     "connectors": [{
      "connector": {
       "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:0]",
       "id": "CDID:0",
       "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
      },
      "in-operator-id": "ODID:1",
      "in-operator-port": 0,
      "out-operator-id": "ODID:0",
      "out-operator-port": 0
     }],
     "operators": [
      {
       "display-name": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor[ODID:0]",
       "id": "ODID:0",
       "in-arity": 1,
       "java-class": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor",
       "out-arity": 0,
       "partition-constraints": {"count": "1"}
      },
      {
       "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:1]",
       "id": "ODID:1",
       "in-arity": 0,
       "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
       "micro-operators": [
        "ets",
        "assign [0] := [edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$ScalarEvaluatorFactoryAdapter@77590662]"
       ],
       "out-arity": 1,
       "partition-constraints": {"count": "1"}
      }
     ]
    }
    [PARTITION_COUNT(ODID:1) in CONSTANT[1:java.lang.Integer], PARTITION_COUNT(ODID:0) in CONSTANT[1:java.lang.Integer]]

#### 2.2 List Query
**Input**:

	let $messages := ['hi' , 'ho', 'hey']
	for $message in $messages
	return $message
	
**Output**:

	"hi"
	"ho"
	"hey"

**Logical Plan**:

    1 distribute result [%0->$$1] -- |UNPARTITIONED|
    2     project ([$$1]) -- |UNPARTITIONED|
    3         unnest $$1 <- function-call: asterix:scan-collection, Args:[%0->$$0] -- |UNPARTITIONED|
    4             assign [$$0] <- [function-call: asterix:ordered-list-constructor, Args:[AString: {hi}, AString: {ho}, AString: {hey}]] -- |UNPARTITIONED|
    5                 empty-tuple-source -- |UNPARTITIONED|

**Hyracks Job**:
    
    {   
     "connectors": [{
      "connector": {
       "display-name": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor[CDID:0]",
       "id": "CDID:0",
       "java-class": "edu.uci.ics.hyracks.dataflow.std.connectors.OneToOneConnectorDescriptor"
      },  
      "in-operator-id": "ODID:1",
      "in-operator-port": 0,
      "out-operator-id": "ODID:0",
      "out-operator-port": 0
     }], 
     "operators": [
      {   
       "display-name": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor[ODID:0]",
       "id": "ODID:0",
       "in-arity": 1,
       "java-class": "edu.uci.ics.hyracks.dataflow.std.result.ResultWriterOperatorDescriptor",
       "out-arity": 0,
       "partition-constraints": {"count": "1"}
      },  
      {   
       "display-name": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor[ODID:1]",
       "id": "ODID:1",
       "in-arity": 0,
       "java-class": "edu.uci.ics.hyracks.algebricks.runtime.operators.meta.AlgebricksMetaOperatorDescriptor",
       "micro-operators": [
        "ets",
        "assign [0] := [edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$ScalarEvaluatorFactoryAdapter@1b625a2d]",
        "unnest 1 <- edu.uci.ics.hyracks.algebricks.core.algebra.expressions.LogicalExpressionJobGenToExpressionRuntimeProviderAdapter$UnnestingFunctionFactoryAdapter@560e4e66",
        "stream-project [1]"
       ],   
       "out-arity": 1,
       "partition-constraints": {"count": "1"}
      }    
     ]    
    }    
    [PARTITION_COUNT(ODID:0) in CONSTANT[1:java.lang.Integer], PARTITION_COUNT(ODID:1) in CONSTANT[1:java.lang.Integer]]

#### 2.3 Join + Aggregation Query
**Dataset**:

	drop dataverse Demo if exists;
	create dataverse Demo;
    use dataverse Demo;
	create type CustomerType as closed {
    	mkt_segment : string,
	    cust_key : int32
	};
	create type OrderType as closed {
		cust_key : int32,
		order_key : int32
	};
    create internal dataset Customers(CustomerType) primary key cust_key;
    create internal dataset Orders(OrderType) primary key order_key;
    insert into dataset Customers([
    	{
	    	"mkt_segment" : "shoes",
    		"cust_key": 0
    	},
    	{
	    	"mkt_segment" : "shoes",
    		"cust_key": 1
    	},
    	{
	    	"mkt_segment" : "pencils",
    		"cust_key": 2
    	}
    ]);
    insert into dataset Orders([
    	{
	    	"order_key" : 0,
    		"cust_key": 0
    	},
    	{
	    	"order_key" : 1,
    		"cust_key": 0
    	},
    	{
	    	"order_key" : 2,
    		"cust_key": 1
    	},
    	{
	    	"order_key" : 3,
    		"cust_key": 2
    	}
    ]);

**Dataverse Check**:

	use dataverse Demo;
    for $customer in dataset Customers
    return $customer;
    for $order in dataset Orders
    return $order;

**Input**:

	use dataverse Demo;
	for $c in dataset Customers
	for $o in dataset Orders
	where $c.cust_key = $o.cust_key
	group by $segment := $c.mkt_segment with $o
	return {
    	"orders" : count($o),
	    "segment" : $segment
	}

**Logical Plan**:

    distribute result [%0->$$11] -- |UNPARTITIONED|
      project ([$$11]) -- |UNPARTITIONED|
        assign [$$11] <- [function-call: asterix:open-record-constructor, Args:[AString: {orders}, function-call: asterix:count, Args:[%0->$$10], AString: {segment}, %0->$$2]] -- |UNPARTITIONED|
          group by ([$$2 := function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {mkt_segment}]]) decor ([]) {
                    aggregate [$$10] <- [function-call: asterix:listify, Args:[%0->$$3]] -- |UNPARTITIONED|
                      nested tuple source -- |UNPARTITIONED|
                 } -- |UNPARTITIONED|
            select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {cust_key}], function-call: asterix:field-access-by-name, Args:[%0->$$3, AString: {cust_key}]]) -- |UNPARTITIONED|
              unnest $$3 <- function-call: asterix:dataset, Args:[AString: {Orders}] -- |UNPARTITIONED|
                unnest $$0 <- function-call: asterix:dataset, Args:[AString: {Customers}] -- |UNPARTITIONED|
                  empty-tuple-source -- |UNPARTITIONED|

**Optimizated Query Plan**:

One can notice the use of a `HashJoin`, absent from the unoptimized plan.

    distribute result [%0->$$11]
    -- DISTRIBUTE_RESULT  |PARTITIONED|
      exchange 
      -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
        project ([$$11])
        -- STREAM_PROJECT  |PARTITIONED|
          assign [$$11] <- [function-call: asterix:closed-record-constructor, Args:[AString: {orders}, %0->$$18, AString: {segment}, %0->$$2]]
          -- ASSIGN  |PARTITIONED|
            exchange 
            -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
              group by ([$$2 := %0->$$20]) decor ([]) {
                        aggregate [$$18] <- [function-call: asterix:agg-sum, Args:[%0->$$19]]
                        -- AGGREGATE  |LOCAL|
                          nested tuple source
                          -- NESTED_TUPLE_SOURCE  |LOCAL|
                     }
              -- PRE_CLUSTERED_GROUP_BY[$$20]  |PARTITIONED|
                exchange 
                -- HASH_PARTITION_MERGE_EXCHANGE MERGE:[$$20(ASC)] HASH:[$$20]  |PARTITIONED|
                  group by ([$$20 := %0->$$13]) decor ([]) {
                            aggregate [$$19] <- [function-call: asterix:agg-count, Args:[AInt64: {1}]]
                            -- AGGREGATE  |LOCAL|
                              nested tuple source
                              -- NESTED_TUPLE_SOURCE  |LOCAL|
                         }
                  -- SORT_GROUP_BY[$$13]  |PARTITIONED|
                    exchange 
                    -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                      project ([$$13])
                      -- STREAM_PROJECT  |PARTITIONED|
                        exchange 
                        -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                          join (function-call: algebricks:eq, Args:[%0->$$14, %0->$$17])
                          -- HYBRID_HASH_JOIN [$$14][$$17]  |PARTITIONED|
                            exchange 
                            -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                              project ([$$13, $$14])
                              -- STREAM_PROJECT  |PARTITIONED|
                                assign [$$13] <- [function-call: asterix:field-access-by-index, Args:[%0->$$0, AInt32: {0}]]
                                -- ASSIGN  |PARTITIONED|
                                  exchange 
                                  -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                                    data-scan []<-[$$14, $$0] <- Demo:Customers
                                    -- DATASOURCE_SCAN  |PARTITIONED|
                                      exchange 
                                      -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                                        empty-tuple-source
                                        -- EMPTY_TUPLE_SOURCE  |PARTITIONED|
                            exchange 
                            -- HASH_PARTITION_EXCHANGE [$$17]  |PARTITIONED|
                              project ([$$17])
                              -- STREAM_PROJECT  |PARTITIONED|
                                assign [$$17] <- [function-call: asterix:field-access-by-index, Args:[%0->$$3, AInt32: {0}]]
                                -- ASSIGN  |PARTITIONED|
                                  project ([$$3])
                                  -- STREAM_PROJECT  |PARTITIONED|
                                    exchange 
                                    -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                                      data-scan []<-[$$15, $$3] <- Demo:Orders
                                      -- DATASOURCE_SCAN  |PARTITIONED|
                                        exchange 
                                        -- ONE_TO_ONE_EXCHANGE  |PARTITIONED|
                                          empty-tuple-source
                                          -- EMPTY_TUPLE_SOURCE  |PARTITIONED|

**Hyracks Job Specification**:

Too long to display.
