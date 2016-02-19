## Galindra Joshi comments

This paper constitutes the first proposal of evaluation and rewriting of subqueries using the apply plan operators, which bears the most similarity with our rewriting.



**The exceptional case** The galindra-joshi paper briefly considers queries of the form :

```
select o orderkey,(select c.name from customer where c.custkey = o.custkey)from orders
```

which they identify as "exception" queries, which would generate a run-time error if the output of the subquery has more than 1 value. We suggest that such use case has become a lot more common in the context of query languages for semi-structured data. 

**Classes of Subqueries** : 
Class 1 corresponds to queries that do not require introducing common subexpressions. This is the situation in our rewritings.

Class 2 correponds to the case where additional subexpressions are introduced (identities 5 through 8 from the paper). This will not happen in our case. Why?

**Question**: How does Galindra-Joshi propose to rewrite the exception case?

Galindra Joshi rewrites the "exception" case using max1row (irrelevant in our case) and equivalences (1) and (2). Equivalence (8) and (9) are not so relevant in our case because reordering the GROUP BY NEST above the OUTER JOIN (in NSAAT) is never beneficial (cardinality of the output of the outer join is at least as much as the cardinality of expression r(p,T).
