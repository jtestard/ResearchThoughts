## Garlic Architecture

Garlic serves as the foundation of data integration architectures we will study in this example.

We start with the fundamentals : 

 - Unifying query language (in the case of Garlic, it is SQL)
 - Query optimizer : which decomposes a query into source-annotated fragments.
   - catalog :the contains hints about the data in data sources which will help the query optimizer choose the best plans.
 - wrappers : they validate then transform a fragment into a query in the target data source's native query language.


Capabilities :

 - Middleware Architecture in which the user does not interact with the data stores directly, but with an intermediate data layer.
 - Unifying query language which can be used to query any underlying data store (SQL in the case of Garlic).
 - Query optimizer which decomposes a SQL query into a set of source-annotated fragments which can be executed at a single data source.
 - Wrappers which translate a fragment into a query in the target data source's native query language.

Functionality :

 - *Request-Reply-Compensate* model : 

Original :

```
SELECT c.name
FROM mySQL.customer as c
WHERE (
	SELECT sum(a.price)
	FROM mongoDB.amazon AS a
	WHERE a.customer = c.name
) > (
	SELECT sum(s.order_total)
	FROM mySQL.sales AS s
	WHERE s.cust_key = c.id
);
```

MySQL Fragment (`T1`) :

```
SELECT	c.name AS name,
		c.id AS id
FROM mySQL.customer;
```

MySQL Fragment (`T2`) :

```
	SELECT	s.cust_key AS ref_id,
	sum(s.order_total) AS sum
	FROM	mySQL.sales AS s
	GROUP BY s.cust_key
```

MongoDB (`T2`) :

```
SELECT	a.customer AS ref_name,
		sum(a.price) AS sum
FROM	mongoDB.amazon AS a
GROUP BY a.customer
```

Executor :

```
SELECT t1.name
FROM  T1 t1, T2 t2, T3 t3
WHERE t1.id = t2.ref
AND	  t1.name = t3.ref
AND   t3.sum > t2.sum
```

```
db.amazon.group({ key : 'customer',
reduce : function ( curr, result)
{result.total += curr.price;},
initial : { total : 0 } })
```



```
FROM T1 t1
WHERE 
```

2 Problems : 

1) Integrate the heterogeneous stores despite the data model differences

 1. Data Partitioning
 2. Query Language/Data Model Heterogeneity
 3. Query Capability Heterogeneity

2) Move data between stores to get the extra efficiency

 4. Where to store the data
 5. How to store the data














