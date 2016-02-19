### Good idea about managing multiple use cases

Use cases only differ in terms of the content of the output of expressions E and F. We only need to show one example in which the query pattern appears clearly, and use it in the introduction.

Use cases can appear at the end, after the experiments section and before related work.

The choice of the example is important. It needs to show the saliant features of the rewriting and be directly applicable to one (if possible several) exisiting use cases. The reader should not have to be convinced about the usefulness of the rewriting.

Examples :

| Example | Operators of inner query | Correlation Relationship | Fancy Features |
|-------------------|----------------------------------------|--------------------------|----------------|
| Clerk query | uses sort but not group by | Many-To-Many | No |
| Nation Query | Uses both GROUP BY and ORDER BY | One-To-Many | No |
| Hour Query | Uses groupby aggregation, but not sort | Many-To-Many | UDF |
| Clickstream Query | Uses both GROUP BY and ORDER BY | Many-To-Many | UDF |

Based on the examples above, the Clickstream query is chosen.


### Introduction Writing

##### Analysis of ID IVM paper introduction

**Paragraph 1** : explain what a materialized view and an incremental update are.

**Paragraph 2** : introduce quickly prior work and describe succintly improvement over prior work.

**Paragraph 3** : example showcasing the benefit of the improvement over the prior work (with figures).

**Paragraph 4** : show caveat/drawback over improvement over prior work.

**Paragraph 5** : outline and contribution of paper.

---

#### Our introduction

To present paragraphs 1 and 2 we have two alternatives:

1) Present TAAT and NSAAT and show how NSAAT improves over TAAT

2) Present TAAT but quickly move over to a discussion between NSAAT and DSAAT.

3) Present all three strategies through a running example.   

**Paragraph 1** :

 1. Nested data is of particular importance in the big data world [Quote semi-structured databases which make use of nested data]
 - The semi-structured databases use a various set of languages. Prior work has shown that those languages can be modeled by SQL++.
 - SQL++ is a query language obtained by removing restrictions from SQL (the full SQL++ specification can be found here []). Of particular interest is the ability to have any kind of SQL query in the SELECT clause, which may cause nesting.
 - Show an example of a SQL++ query (running example) using simplified schema from TPC-BB benchmark.

**Paragraph 2** :

 1. This form of queriy presents opportunities for decorrelation.
 - Prior work has focused on the FROM and WHERE clause, where the output was purely relational. In the `SELECT` clause, prior work has focused on cases where the select clause outputs up to one tuple with a single attribute (the only form of subquery allowed in the SELECT clause in SQL).
 - We extend prior work by studying decorrelation on the SELECT clause when the output of the subquery may have multiple attributes and multiple columns.

**Note** : Make sure point 3 is accurate; in particular with respect to DSAAT. Galindra-Joshi is a starting point. 

**Paragraph 3** :

 - We present here two forms of query patterns which have the same attributes o 

**Paragraph 4** :

**Paragraph 5** :

The introduction will have 

 


**Schema figure**

```
product(key, name)
clickstream(product, time)
```


### About R4 (DSAAT)

We need to show it in terms of prior work, making it clear that this is the state of the art in semi-structured databases.

### Physical plans for Cost Model Section

They can help drive the discussion based on the query pattern and example. They introduce one problem: they are scenario and parameter specific. Depending on how scenarios 2 and 3 turn out, we may want to shift the discussion from being scenario based to being physical plan based, since their might be overlap of physical plan between scenarios.