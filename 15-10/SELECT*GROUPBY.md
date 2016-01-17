## SELECT * GROUP BY

#### 1 The problem

Assuming the following dataset :

```
CREATE TABLE FBU (id serial primary key, fname text, lname text);
CREATE TABLE FBM (id serial primary key, contents text, uid integer);

INSERT INTO FBU (id, fname, lname) VALUES (1, 'jules', 'testard');
INSERT INTO FBU (id, fname, lname) VALUES (2, 'gaby', 'abou mehri');
INSERT INTO FBU (id, fname, lname) VALUES (3, 'wissam', 'bettahar');
INSERT INTO FBM (id, uid, contents) VALUES (1, 1, 'hello');
INSERT INTO FBM (id, uid, contents) VALUES (2, 2, 'hi');
INSERT INTO FBM (id, uid, contents) VALUES (3, 2, 'bonjour');
```

We want to ensure that the following query (**Query 1**) will run successfully in SQL++ (by successfully, we mean will yield the same results as if it was run using regular SQL) :

```
SELECT *
FROM FBU u, FBM m
WHERE u.id = m.uid
GROUP BY u.id, m.id;
```

#### 2 What is the expected SQL behavior

We use PostgreSQL as the query language for representing "SQL" behavior. Query 1 is translated by the PostgreSQL query compiler into :

```
SELECT u.id, u.fname, u.lname, m.id, m.uid, m.contents
FROM FBU u, FBM m
WHERE u.id = m.uid
GROUP BY u.id, m.id;
```

This query is then deemed valid because all fields present in the `SELECT` clause can be derived from fields in the `GROUP BY` clause. Query 1 would then execute and yield :

```
 id | fname |   lname    | id | uid | contents
----+-------+------------+----+-----+----------
  1 | jules | testard    |  1 |   1 | hello
  2 | gaby  | abou mehri |  2 |   2 | hi
  2 | gaby  | abou mehri |  3 |   2 | bonjour
(3 rows)
```

#### 3 How the SQL++ behave currently

Recall the definition Yannis gave us (which was only given as an example) :

```
SELECT * FROM r AS x JOIN s AS y

is equivalent to the following core

SELECT ELEMENT tuple_concat(
  (SELECT ATTRIBUTE a : v FROM x AS {a :v}),
   SELECT ATTRIBUTE a : v FROM y AS {a :v}))
FROM r AS x JOIN s AS y
```

From this example, I identified one possible rewriting for the `SELECT *` statement in SQL++:

The `SELECT *` statement is to be replaced with a `tuple_concat` UDF with `n` arguments, where `n` is the number of variable in the scope of the `SELECT` clause. For each such variable `x`, the query `SELECT ATTRIBUTE a : v FROM x AS {a :v}` is produced.

Note that this rewriting will fail if some variable in the scope of the `SELECT` clause is not a tuple (see last paragraph of section 5.1 (1.b) on page 8 of the SQL++ paper). 

If we apply this rewriting to Query 1, we get :

```
SELECT ELEMENT tuple_concat(
	(SELECT ATTRIBUTE a:v FROM u.id AS {a:v}),
	(SELECT ATTRIBUTE a:v FROM m.id AS {a:v}),
	(SELECT ATTRIBUTE a:v FROM group AS {a:v})
)
FROM FBU u, FBM m
WHERE u.id = m.uid
GROUP BY u.id AS uid, m.id AS mid;
```

Which will either result in an error, or an output different from the SQL output (depending on configuration parameters).

The source of the problem seems to be the fact that the rewriting is dependent on the variables in scope to be tuples, when in fact they could be scalars or bags as well.
