## Rewriting Procedures for batched bindings

Questions :

 - What kind of programs can be rewritten using this technique
 - How is a rewriting opportunity identified?
 - How effective is the rewriting?
 - Can we get a declarative description of the rewriting?

 - *Batch-safe* operations: operations which will not be affected by the order in which computations on that object will be perfomed (within a loop). More formally :
   - The operation's return value, for any parameter is independent of the order in which the parameters are being processed.
   - The final system state is independent of the order in which the arguments are processed.

 
##### Query 1 with UDF
 
 ```
 SELECT orderid
 FROM sellorders
 WHERE mkt='NYSE'
 	AND count_offers(itemcode, amount, curcode) > 0;
 	
 INT count_offers( INT itemcode, FLOAT amount, VARCHAR curcode )
 DECLARE
 	FLOAT amount_usd;
 BEGIN
   -- get amount in USD
 	IF (curcode == 'USD')
 		amount_usd = amount;
 	ELSE
 		amount_usd = amount * (
 			SELECT exchrate
 			FROM curexch WHERE ccode;
 		)
 	END IF
 	-- Count # of offers whose price is greater than amount_usd
 	RETURN	SELECT count(*)
 			FROM buyoffers
 			WHERE itemid = itemcode
 				AND price >= amount_usd
 ```
 
##### Iterative plan for Query 1

```
for each t in ( SELECT orderid FROM sellorders WHERE mkt='NYSE')
	if (count_offers(itemcode, amount, curcode) > 0)
		output t.orderid;
end;
```
 
##### Batched form of Query 1 with UDF

```
... [[ too long for the moment ]]
```

### Data dependence Graph

Directed multi-graph in which :

 - Program statments are nodes
 - Edges represent data dependencies between statements

There are four kinds of dependencies :

 - **Flow-Dependency** edge (`=FD=>`) : if `sa` writes to a location from which `sb` reads and `sa` occurs before `sb`, then `sa =FD=> sb`
 - **Anti-Dependency** edge (`=AD=>`): if `sa` reads to a location from which `sb` writes and `sa` occurs before `sb`, then `sa =AD=> sb`
 - **Output-Dependency** edge (`=OD=>`): if `sa` writes to a location from m which `sb` writes and `sa` occurs before `sb`, then `sa =OD=> sb`
 - **Loop-Carried Dependency** edge (`=LFD=>`,`=LAD=>`,`=LOD=>`): 


### What kind of programs can be rewritten using this technique

Batchable programs can be rewritten using this technique. A program is batchable with respect to a loop. We say invocation of operation `q` is *batchable* with respect to loop `L` if it we can remove `q` from a loop body and use a single invocation of a batched form of this operation `qb` outside the loop.

```
for each t in r loop
	q(t.c1, ..., t.cm)
end loop
```

is equivalent to :

```
qb(proj_{c1,...,cm}(r));
```

## Generating Batched Form of procedures

Assume that a side-effect free, batch safe, procedure `f`. We can derive the trivial batch `bf` form :

```
Apply(pt, f):
r = {}
for each t in pt:
	rf = f(t); // f(t) can be inlined
	r.addRecords({t} x rf);
return r;
```
Now in some context, this can be done better.

The paper *does not* describe how to obtain `bf`, instead relies on the "query decorrelation literature". The paper mentions that each operation inside a loop can be separately batched, and each batch operation would have its own batched procedure.

The paper focuses instead on how to transform a program into a form which allows batching.