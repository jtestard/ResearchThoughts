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

 1. Nested data is of particular importance in the big data world. Document stores stemming from the NoSQL movement store, query and produce documents with nested structure. [Quote semi-structured databases which make use of nested data]
 - The semi-structured databases use a various set of languages. Prior work has shown that those languages can be modeled by SQL++.
 - SQL++ is a query language obtained by removing restrictions from SQL (the full SQL++ specification can be found here []). Of particular interest is the ability to have any kind of SQL query in the SELECT clause, which may cause nesting.
 - Show an example of a SQL++ query (running example) using simplified schema from TPC-BB benchmark.

```
SELECT s.supplierkey, s.name, (           SELECT p.brand, count(*) AS total           FROM part AS p, partsupp AS ps           WHERE s.suppkey = ps.suppkey
           AND ps.partkey = p.partkey           GROUP BY p.brand           ORDER BY total DESC           LIMIT 3       ) AS aggregatesFROM supplier AS s LIMIT L;
```

**Paragraph 2** :

 1. This form of queriy presents opportunities for decorrelation.
 - Prior work has focused on the FROM and WHERE clause, where the output was purely relational. In the `SELECT` clause, prior work has focused on cases where the select clause outputs up to one tuple with a single attribute (the only form of subquery allowed in the SELECT clause in SQL).
 - We extend prior work by studying decorrelation on the SELECT clause when the output of the subquery may have multiple attributes and multiple columns.

**Note** : Make sure point 3 is accurate; in particular with respect to DSAAT. Galindra-Joshi is a starting point. 

**Paragraph 3** :

 - We present here the NSAAT and DSAAT query evaluations.

1) Describe NSAAT query.

```
CREATE TEMPORARY TABLE T AS (
	SELECT DISTINCT suppkey
	FROM supplier
	LIMIT L
);

SELECT t1.suppkey, t1.suppname, (
	CASE t2 IS NULL THEN [] ELSE t2
)
FROM T AS t1 LEFT OUTER JOIN (
	SELECT t2.suppkey, NEST(brand, total) AS N
	FROM (
		SELECT t2.suppkey, brand, total,
			row_number() OVER (
			  PARTITION BY t2.suppkey
			  ORDER BY total DESC) AS rn
		FROM (
			SELECT p.brand, COUNT(*) AS total, 
			FROM part AS p, partsupp AS ps, T AS t2
			WHERE t2.suppkey = ps.suppkey
			AND ps.partkey = p.partkey
			GROUP BY t2.suppkey, p.brand
		) AS i1
	) AS i2
	WHERE rn <= 3
	GROUP BY t2.suppkey
) AS i3
ON t1.suppkey = t2.suppkey;
```

Time-delta function is simply a short for computing the absolute value. 

2) Describe DSAAT query : 

```

```

3) We explain how NSAAT and DSAAT can provide  

**Paragraph 4** :

Describe the outline 


**Schema figure**
