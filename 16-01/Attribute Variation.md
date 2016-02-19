## Attribute variation

The performance evaluation of expressions R0, R2 and R4 depend on the of the architecture, query and data parameters on which the rewriting is performed.

We classify each parameter into one of three categories: 

 1. Parameters which remain at constant value for the entirety of the evaluation.
 - Parameters whose value is varied a discrete number of distinct settings.
 - Parameters for which no assumption is made

Classification decisions are based on reasonable assumptions based on real-world usage of the rewriting.


1) Attributes which remain constant:

 - Query operators : in inner query of tuple-at-a-time formulation, we assume presence of a GROUP BY, ORDER BY and LIMIT clauses, as well as limiting correlation to the WHERE clause, in the form of an equality predicate `e.c = f.c`
 - Output of plan P is small (reasonable assumption)
 - k value for top-k is small (reasonable assumption)

2) Attributes which vary:

 - Size of expression *E*: chosen because it is an attribute which describes precisely the difference between scenarios 1 and 2.
 - Size of expression *F*: chosen because it is an attribute which describes precisely the difference between scenarios 1 and 2.
 - Size of *V(c,F)*: chosen because it determines the size of the output of the join. A large join wil
 - Size of *V(c,E)*: chosen because it determines the number of duplicate correlated subplans in R0 and highlights the advantage of R2. 

3) Attributes for which no assumption is made:

 - number of distinct grouping attribute values for the GROUP BY clause `V(g,F)`: a low value of `V(g,F)` will cause a change from external to in-memory sorting for the tau operator execution, while a high value may not. We ignore this effect.

### Investigation for reasonable values and assumptions

Query 2 from TPC-BB

```
SELECT p1.name, (
    SELECT p2.name, COUNT(s2.key)
    FROM clickstream cs1,
         clickstream cs2,
         products p2
    WHERE p1.key = cs1.produc
    AND time-delta(cs1.time,cs2.time) < 60
    AND cs2.product = p2.key
    GROUP BY p2.key
    ORDER BY count
    LIMIT 30
) AS top30
FROM selected_products p1;
```

Data Characteristics :

 - |E| is small (let's say 10 selected products)
 - products is 10k rows
 - clickstream is 100M
 - |F| is very large (1B rows)
 - V(c,F) is small 

### Things that should be clear from the presentation

1) We are evaluating R0, R2 and R4 and describing which one is best in which scenario

2) We describe and fix query parameters besides the following 4:
 E F V(c,E) and V(c,F)
 
3) Each scenario fixes E and F and describes characteristics when varying V(c,E) and V(c,F)


Make the SQL++ query pattern, and use it to help make assumptions for the input.

We evaluate the performance of query pattern using query plan formulations R0, R2 and R4.