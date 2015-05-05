### Set-at-a-time rewriting gone wrong

Here is a problem we encounter when trying to apply a normalized set rewriting on a SQL++ query with a subquery in the `SELECT` clause in Asterix.

Assume the following SQL++ environment :

```
Nations = {{
	{ nation_key : 1, nation_name : "USA" },
	{ nation_key : 2, nation_name : "China" }
}}

Customers = {{
	{ cust_key : 1, nation_ref : 1, amount_spent : 20}
	{ cust_key : 2, nation_ref : 1, amount_spent : 40}
}}
```

Consider the following SQL++ tuple-at-a-time query, which gives
for each nation the average amount spent by its customers :

```
use dataverse GlobalMarketplace;

SELECT  n.nation_name AS name,
		(  
			SELECT ELEMENT sum(c.amount_spent)
			FROM Customers AS c
			WHERE c.nation_ref = n.nation_key
			GROUP BY n.nation_key AS id
		) AS amount_spent
FROM 	Nations AS n;

Result :
{ name : "USA", "amount_spent" : {{ 60 }} }
{ name : "China", "amount_spent" : {{ }} }
```

And its almost set-at-a-time counterpart :

```
use dataverse GlobalMarketplace;

SELECT	l.nation_name AS nation_name,
		r.N AS amount_spent
FROM 	Nations AS l
LEFT OUTER JOIN (
	SELECT nid as nid,
	       (SELECT ELEMENT g.x.spent FROM group AS g) as N
    FROM ( SELECT nid as nid,
			    sum(c.amount_spent) AS spent
	  FROM Customers as c, Nations as n
	  WHERE c.nation_ref = n.nation_key
	  GROUP BY n.nation_key as nid
	) AS x
	GROUP BY x.nid as nid
) as r
ON l.nation_key = r.nid;

Result :
{ name : "USA", "dollar_spent" : {{ 60 }} }
{ name : "China", "dollar_spent" : missing }
```

\* : where `group.x.spent` evaluates to `(SELECT ELEMENT g.x.spent FROM group as g)`.

It is not quite possible to generate exactly the decorrelation rewriting using SQL++, because the rewriting happens on algebra, and the decorrelation rewriting algebraic plan can't quite be rewritten using Asterix.