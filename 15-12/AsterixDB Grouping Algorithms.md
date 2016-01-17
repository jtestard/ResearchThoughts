# AsterixDB Grouping Algorithms


In the running example, the sub plan is transformed into a group by listify using the **pre-clustered group by** approach. 


### Alternate plan for Asterix

Consider the following asterix pseudo-plan:

```
Group By Grouping Key {
	agg_var <- listify
		Nested Tuple Source
}
	Select rn < LIMIT value
		Sort by Grouping Key, Order By Key, rowNumber -> rn
			Expression E
```

### Row Order By

The `row_order_by(...)` operation is applied by iterating over a sorted list. Similar to the positional index, but its value is resetted to 1 applied when the values of the argument attribute set change from iteration i to iteration j. 

### Cost Model Discussion

We revise cost-model for middleware:

 - TAAT cost model (existing)
 - Normalized SAAT cost model (existing)
 - Denormalized SAAT cost model (existing)

We evaluate the cost models for possible AsterixDB rewritings.



Given some assumptions, we add a alternate rewriting using the `row_order_by()` operator