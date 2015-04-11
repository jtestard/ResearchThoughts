### Absent type in query

#### SQL++ Query 

```
use dataverse GlobalMarketplace;
	WITH (
		SELECT 	nation_key AS nation_key,
				order_year AS order_year,
	            sql-sum (
	                ( SELECT ELEMENT g.o.total_price
	                  FROM group as g )
	            ) AS list_price
		FROM 	Nations as n,
				Orders as o,
				Customers as c
		WHERE 	n.nation_key = c.nation_ref AND c.cust_key = o.cust_ref
		GROUP BY 	o.order_year as order_year,
					n.nation_key as nation_key
	) AS price_per_year
	SELECT	nation_key as nation_key,
			(
				SELECT 	g.ppy.order_year AS order_year,
						g.ppy.list_price AS list_price
				FROM group as g
				ORDER BY g.ppy.order_year DESC
				LIMIT 3
			) AS aggregates
	FROM	price_per_year AS ppy
	GROUP BY	ppy.nation_key AS nation_key;
```

General opinion : the frame limit makes it harder to handle large groupings.


#### Initial Plan

```
distribute result [%0->$$35] -- |UNPARTITIONED|
  project ([$$35]) -- |UNPARTITIONED|
    assign [$$35] <- [function-call: asterix:open-record-constructor, Args:[AString: {nation_key}, %0->$$9, AString: {aggregates}, %0->$$40]] -- |UNPARTITIONED|
      subplan {
                aggregate [$$40] <- [function-call: asterix:listify, Args:[%0->$$37]] -- |UNPARTITIONED|
                  assign [$$37] <- [function-call: asterix:open-record-constructor, Args:[AString: {order_year}, function-call: asterix:field-access-by-name, Args:[%0->$$11, AString: {order_year}], AString: {list_price}, function-call: asterix:field-access-by-name, Args:[%0->$$11, AString: {list_price}]]] -- |UNPARTITIONED|
                    limit AInt32: {3} -- |UNPARTITIONED|
                      order (DESC, function-call: asterix:field-access-by-name, Args:[%0->$$11, AString: {order_year}])  -- |UNPARTITIONED|
                        unnest $$11 <- function-call: asterix:scan-collection, Args:[%0->$$34] -- |UNPARTITIONED|
                          nested tuple source -- |UNPARTITIONED|
             } -- |UNPARTITIONED|
        group by ([$$9 := function-call: asterix:field-access-by-name, Args:[%0->$$8, AString: {nation_key}]]) decor ([]) {
                  aggregate [$$34] <- [function-call: asterix:listify, Args:[%0->$$10]] -- |UNPARTITIONED|
                    nested tuple source -- |UNPARTITIONED|
               } -- |UNPARTITIONED|
          assign [$$10] <- [function-call: asterix:open-record-constructor, Args:[AString: {ppy}, %0->$$8, AString: {price_per_year}, %0->$$0]] -- |UNPARTITIONED|
            unnest $$8 <- function-call: asterix:scan-collection, Args:[%0->$$0] -- |UNPARTITIONED|
              assign [$$0] <- [%0->$$31] -- |UNPARTITIONED|
                subplan {
                          aggregate [$$31] <- [function-call: asterix:listify, Args:[%0->$$26]] -- |UNPARTITIONED|
                            assign [$$26] <- [function-call: asterix:open-record-constructor, Args:[AString: {nation_key}, %0->$$5, AString: {order_year}, %0->$$4, AString: {list_price}, function-call: asterix:sql-sum, Args:[%0->$$30]]] -- |UNPARTITIONED|
                              subplan {
                                        aggregate [$$30] <- [function-call: asterix:listify, Args:[%0->$$29]] -- |UNPARTITIONED|
                                          assign [$$29] <- [function-call: asterix:field-access-by-name, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$7, AString: {o}], AString: {total_price}]] -- |UNPARTITIONED|
                                            unnest $$7 <- function-call: asterix:scan-collection, Args:[%0->$$25] -- |UNPARTITIONED|
                                              nested tuple source -- |UNPARTITIONED|
                                     } -- |UNPARTITIONED|
                                group by ([$$4 := function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {order_year}]; $$5 := function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {nation_key}]]) decor ([]) {
                                          aggregate [$$25] <- [function-call: asterix:listify, Args:[%0->$$6]] -- |UNPARTITIONED|
                                            nested tuple source -- |UNPARTITIONED|
                                       } -- |UNPARTITIONED|
                                  assign [$$6] <- [function-call: asterix:open-record-constructor, Args:[AString: {c}, %0->$$3, AString: {n}, %0->$$1, AString: {o}, %0->$$2]] -- |UNPARTITIONED|
                                    select (function-call: algebricks:and, Args:[function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {nation_key}], function-call: asterix:field-access-by-name, Args:[%0->$$3, AString: {nation_ref}]], function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$3, AString: {cust_key}], function-call: asterix:field-access-by-name, Args:[%0->$$2, AString: {cust_ref}]]]) -- |UNPARTITIONED|
                                      unnest $$3 <- function-call: asterix:dataset, Args:[AString: {Customers}] -- |UNPARTITIONED|
                                        unnest $$2 <- function-call: asterix:dataset, Args:[AString: {Orders}] -- |UNPARTITIONED|
                                          unnest $$1 <- function-call: asterix:dataset, Args:[AString: {Nations}] -- |UNPARTITIONED|
                                            nested tuple source -- |UNPARTITIONED|
                       } -- |UNPARTITIONED|
                  empty-tuple-source -- |UNPARTITIONED|
```

I get this error during the optimization :

```
Could not infer type for variable '$$40'. [AlgebricksException]
```

### DEBUG ouptut

```
        @Override
        public ClosedDataInfo visitVariableReferenceExpression(VariableReferenceExpression expr, Void arg)
                throws AlgebricksException {
            Object varType = env.getVarType(expr.getVariableReference());
            if (varType == null) {
>>(DEBUG)                throw new AlgebricksException("Could not infer type for variable '" + expr.getVariableReference()
                        + "'.");
            }
            boolean dataIsClosed = isClosedRec((IAType) varType);
            return new ClosedDataInfo(false, dataIsClosed, expr);
        }
```

with the `env.varTypeMap = {}`

My analysis seems to indicate this error is caused by a `VariableReferenceExpression` having no type.
