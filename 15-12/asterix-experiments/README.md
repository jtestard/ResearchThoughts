# AsterixExperimentsGenerator

### Results


#### Small Dataset

 - 10 Nations
 - 100 Customers
 - 1000 Orders

Original Query time : 0.722 sec
Rewritten Query time : 0.337 secy

Dump data access demo backup using from postgres into json

```
demo=# COPY (Select row_to_json(t) FROM (SELECT * FROM tpch.nation) AS t) to '/Users/julestestard/Projects/ResearchThoughts/15-12/asterix-experiments/nations.adm';
COPY 25
demo=# COPY (Select row_to_json(t) FROM (SELECT * FROM tpch.customers) AS t) to '/Users/julestestard/Projects/ResearchThoughts/15-12/asterix-experiments/customers.adm';
COPY 1500
demo=# COPY (Select row_to_json(t) FROM (SELECT * FROM tpch.orders) AS t) to '/Users/julestestard/Projects/ResearchThoughts/15-12/asterix-experiments/orders.adm';
COPY 15000
```

## Queries for demo for Friday December 18th

For each order, we want :

 - Order amount
 - Clerk name
 - Top 3 orders made by same clerk

Characteristics of query:

 - Order By within nested query
 - correlated attribute not unique

Two questions:

 - What are the conditions on rewriting ?
 - What are the physical execution characteristics of group-by apply plan approach (if they suck, maybe it's worth it to improve them or make an partition by physical operator)

#### Comments on the analysis

 - Is it the case that a join algorithm and an aggregation algorithm may be pipelined
   - The assumption here is that they are not pipelined (requires write then read if spills on disk)
 - Data already in memory should be written to help clarify
 - If the cost of an in-memory physical operator is 0, it is assumed that the output of the previous operator is in memory before processing starts
 - Cost of writing eventual result to file is not taken into account here.
 - Join algorithm issue clarified.
 - Rewritings are correct even when there are no correlated attributes, as long as projection of no attributes produces an empty output tuple for each input tuple.
 - "Copy" price for rewritings 1-3 includes both writing the output of E to a temporary table and reading this output back for further processing.

### Original query:

#### FORWARD
```
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, (
    SELECT o2.o_totalprice AS price
    FROM db.orders AS o2
    WHERE o.o_clerk = o2.o_clerk
    ORDER BY price DESC
    LIMIT 3
) AS other_orders
FROM (
	SELECT o.*
	FROM db.orders AS o
	ORDER BY o.o_orderkey
	LIMIT 10
) AS o;
```

#### Asterix

Original :

```
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, (
    SELECT o2.o_totalprice AS price
    FROM tpch.Orders AS o2
    WHERE o.o_clerk = o2.o_clerk
    ORDER BY o2.o_totalprice DESC
    LIMIT 3
) AS other_orders
FROM tpch.Orders AS o;
```

With limit :

```
WITH (
	SELECT ELEMENT o
	FROM tpch.Orders AS o
	ORDER BY o.o_orderkey
	LIMIT 10
) AS Tmp
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, (
    SELECT o2.o_totalprice AS price
    FROM tpch.Orders AS o2
    WHERE o.o_clerk < o2.o_clerk
    ORDER BY o2.o_totalprice DESC
    LIMIT 3
) AS other_orders
FROM Tmp AS o;
```

### Semi-join rewriting:


#### FORWARD
```
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, rhs.orders AS other_orders
FROM db.orders AS o
LEFT OUTER JOIN (
	SELECT t.clerk AS clerk, (
	    SELECT o2.o_totalprice AS price
	    FROM db.orders AS o2
	    WHERE o2.o_clerk = t.clerk
	    ORDER BY price DESC
	    LIMIT 3
	) AS orders
	FROM (
		SELECT DISTINCT e.o_clerk AS clerk
		FROM db.orders AS e
	) AS t
) AS rhs
ON o.o_clerk = rhs.clerk
```


#### AsterixDB

```
WITH (
	SELECT ELEMENT o
	FROM tpch.Orders AS o
	ORDER BY o.o_orderkey
	LIMIT 10
) AS Tmp
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, rhs.orders AS other_orders
FROM Tmp AS o
LEFT OUTER JOIN (
	SELECT t.clerk AS clerk, (
	    SELECT o2.o_totalprice AS price
	    FROM tpch.Orders AS o2
	    WHERE o2.o_clerk = t.clerk
	    ORDER BY o2.o_totalprice DESC
	    LIMIT 3
	) AS orders
	FROM (
		SELECT clerk
		FROM tpch.Orders AS e
		GROUP BY e.o_clerk AS clerk
	) AS t
) AS rhs
ON o.o_clerk = rhs.clerk;
```

#### Tmp

```
SELECT  c.clerk AS clerk, (
    SELECT o2.o_totalprice AS price
    FROM tpch.Orders AS o2
    WHERE c.clerk = o2.o_clerk
    ORDER BY o2.o_totalprice DESC
    LIMIT 3
) AS top_orders
FROM (
  SELECT clerk
  FROM tpch.Orders AS o
  GROUP BY o.o_clerk AS clerk
) AS c;
```

 - Join on clerk 
 - Group on distinct clerk

```
SELECT  c.clerk AS clerk, (
    SELECT o2.o_totalprice AS price
    FROM tpch.Orders AS o2
    WHERE c.clerk = o2.o_clerk
    ORDER BY o2.o_totalprice DESC
    LIMIT 3
) AS top_orders
FROM (
  SELECT o.o_clerk AS clerk
  FROM tpch.Orders AS o
) AS c;
```

 - Join on clerk
 - Group on primary key

```
```

### Rewriting 3

#### AsterixDB

```
SELECT o.o_totalprice AS price, o.o_clerk AS clerk, rhs.orders AS other_orders
FROM tpch.Orders AS o
LEFT OUTER JOIN (
	SELECT clerk AS clerk, (
	    SELECT g.o2.o_totalprice AS price
	    FROM group AS g
	    ORDER BY g.o2.o_totalprice DESC
	    LIMIT 3
	) AS orders
	FROM tpch.Orders AS o1
        JOIN tpch.Orders AS o2
        ON o1.o_clerk < o2.o_clerk
        GROUP BY o1.o_clerk AS clerk
) AS rhs
ON o.o_clerk = rhs.clerk;
```



## Other queries

```
use dataverse TinySocial;

select user.name, (
   select element emp."organization-name"
   from user.employment AS emp
) AS org
from FacebookUsers as user
where user.id = 8;
```