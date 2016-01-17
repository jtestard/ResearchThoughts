## Gurst Vs Cheung

We are right this document to compare and contrast the approaches taken by Torsten Gurst's lab and Alvin Cheung to query unnesting.

Criteria : 

 - Runtime : how fast can the rewriting be made.
 - Performance : what is the improvement to performance.
 - Expressiveness of rewriting : how expressive is the technique
 - Adaptability : what code can the technique be run on? Does the technique have any required dependencies?
 - Is it straightforward to change to adapt those techniques to SQL++?

#### Order

Order does not matter 

### Runtime

##### Time to run analysis/rewriting

 - Order of milliseconds for Ferry/Switch.
 - Order of minutes for Cheung

##### Rewriting occurs

 - Ferry: at compile time
 - Switch: at runtime
 - Cheung : analysis as a preprocessing step before compilation.

### Performance

### Expressiveness

### Adapatibility

 - Gurst's Ferry-based query compiler (LINQ, Ferry, Switch) operate by transforming the LINQ/Ferry statements into a plan through loop lifting, there is no analysis step. It is through expression inference based on context that the algebraic plan is produced.
 - Such plans are very complex, and extra steps need to be taken to simplify them. 
 - A special syntax is required.
 - LINQ by itself already provides query capabilities over at least SQL, session and XML data. Avalanche-Safe LINQ uses inference rules to convert a chain of LINQ SQOs into an algebraic plan.

Ferry/LINQ might not be an ideal candidate, because the advantage of introducing SQL++ (application level query compiler with broad set of rewriting rules for semi-structured data) is partially lost. Indeed, LINQ is already playing the role FORWARD would be playing in this situation (middleware), although maybe not as well. Also, the second advantage we are looking for is to make Forward as adaptable as possible to existing code (away from a specialized syntax), which is exactly what both Avalanche-safe LINQ and Switch require.


#### Switch vs Ferry-LINQ

In LINQ, a multi-line statement is transformed by the query compiler into a chain of SQO invocations.

Switch uses abstract interpretation to replicate this "chain of operation" using a code. 

##### Hypothesis

Does Switch expression tree allow to transform this :

```
discount = 20.0/100
high_vol = 10
high_vols = Order.group_by(&:user_id)
					.select {|u,os| os.length >= high_vol}
open_orders = high_vols.map {|u,os| os.select 
						{|o| o.state == "0"}}.flatten
items = open_orders.map {|o| line_item.in_order(o)}.flatten
cost = items.sum {|i| i.price * i.quantity} * discount
```

into that :

```
cost = Order.group_by(&:user_id)
	.select {|u,os| os.length >= high_vol}
	.map {|u,os| os.select {|o| o.state == "0"}}.flatten
	.map {|o| line_item.in_order(o)}.flatten
	.sum {|i| i.price * i.quantity} * (20.0/100)
```