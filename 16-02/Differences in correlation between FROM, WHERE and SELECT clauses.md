## Differences in correlation between FROM, WHERE and SELECT clauses

### FROM clause

Cannot contain correlation from other items of the `FROM` clause, it is therefore not a target for decorrelation.

### GROUP BY and ORDER BY clauses

The GROUP BY and ORDER BY clauses in SQL require attribute arguments, not expressions, therefore there cannot be a subquery in a GROUP BY or ORDER BY clause.

### LIMIT and OFFSET clauses

Correlated Subqueries can occur but these are "fringe" cases (don't occur so much in practice). There are also not allowed in SQL (or at least not in postgres).

### WHERE clause

This is the case which has been most studied in previous work. Within the where clause, sub-queries can occur either in terms comparison:

 - Equality and inequality predicates
 - Existential/Universal Quantifiers quantifiers
 - Control flow predicates

### SELECT clause

Correlated subqueries may appear as select items in the `SELECT` clause. In traditional relational SQL, the `SELECT` clause subqueries output up to one tuple with a single attribute. In SQL++, those subqueries may have any form. In the case where the output has multiple rows/attributes, a nested collection is formed.