### Good idea about managing multiple use cases

Use cases only differ in terms of the content of the output of expressions E and F. We only need to show one example in which the query pattern appears clearly, and use it in the introduction.

Use cases can appear at the end, after the experiments section and before related work.

The choice of the example is important. It needs to show the saliant features of the rewriting and be directly applicable to one (if possible several) exisiting use cases. The reader should not have to be convinced about the usefulness of the rewriting.

Examples :

| Example           | Operators of inner query               | Correlation Relationship | Fancy Features | Number of relations in subquery |
|-------------------|----------------------------------------|--------------------------|----------------|---------------------------------|
| Clerk query       | uses sort but not group by             | Many-To-Many             | No             | 1                               |
| Nation Query      | Uses both GROUP BY and ORDER BY        | One-To-Many              | No             | 2                               |
| Hour Query        | Uses groupby aggregation, but not sort | One-To-Many              | UDF            | 1                               |
| Clickstream Query | Uses both GROUP BY and ORDER BY        | Many-To-Many             | UDF            | 3                               |
| Supplier query    | Uses both GROUP BY and ORDER BY        | Many-To-Many             | No             | 2                               |

The supplier query is chosen because:

 - It has both GROUP BY and ORDER BY in inner query.
 - Its correlation relationship is a many-to-many
 - It does not have any fancy features (UDFs...)
 - The number of relations in the inner query is small (makes more concise plans on the paper).

### Supplier Query

```
SELECT s_supplierkey, s_name, (           SELECT p_brand, count(*) AS total           FROM part, partsupp           WHERE s_suppkey = ps_suppkey
           AND ps_partkey = p_partkey           GROUP BY p_brand           ORDER BY total DESC           LIMIT 3       ) AS aggregatesFROM supplier LIMIT L;
```

### Look at existing nested query example in document store use cases

**Note**: in examples, we notice that correlated attributes are often keys. When they are not keys, they are often part of a bigger join.

### About R4 (DSAAT)

We need to show it in terms of prior work, making it clear that this is the state of the art in semi-structured databases.

### Physical plans for Cost Model Section

They can help drive the discussion based on the query pattern and example. They introduce one problem: they are scenario and parameter specific. Depending on how scenarios 2 and 3 turn out, we may want to shift the discussion from being scenario based to being physical plan based, since their might be overlap of physical plan between scenarios.