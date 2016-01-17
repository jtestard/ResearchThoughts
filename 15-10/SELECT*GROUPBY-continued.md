#### 1 For the Postgres query,  what if a group contains multiple tuples?

PostgreSQL prevents this possibility, because it requires all fields in the select clause to be either 1) mentioned in the `GROUP BY` clause (or can be uniquely derived from a field in the group by clause) 2) included in an aggregation.

Say we changed slightly **Query 1** into the following (which we call **Query 2**) :

```
SELECT *
FROM FBU u, FBM m
WHERE u.id = m.uid
GROUP BY u.id;
```

Query 2 would then be translated by the PostgreSQL query compiler into :

```
SELECT u.id, u.fname, u.lname, m.id, m.uid, m.contents
FROM FBU u, FBM m
WHERE u.id = m.uid
GROUP BY u.id;
```

And then would throw the error :

```
ERROR:  column "m.id" must appear in the GROUP BY clause 
or be used in an aggregate function
LINE 1: SELECT *
```

Under these conditions, there can never be a group with multiple tuples. Now this is just for PostgreSQL, I don't know enough about how other DBMS deal with this situation.

#### 2  Fundamental question

Assuming "SQL backwards-compatible" is the same as "PostgreSQL backwards-compatible" (ignoring other relational RDBMS) and assuming the data outputted by the `FROM` clause is flat, the group variable is guaranteed to contain a single flat tuple, which solves your fundamental question dilemma.

If the data outputted by the `FROM` clause is not flat, then I guess you need to define an expected behavior. This begs the question of how to combine a SQL backwards-compatible construct (such as "*"), is used with a purely SQL++ construct.