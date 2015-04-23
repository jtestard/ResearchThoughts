### Set-at-a-time rewriting gone wrong

Here is a problem we encounter when trying to apply a normalized set rewriting on a SQL++ query with a subquery in the `SELECT` clause in Asterix.

Assume the following SQL++ environment :

```
Nations = {{
	{ id : 1, name : "USA" },
	{ id : 2, name : "China" }
}}

Customers = {{
	{ id : 1, nation_ref : 1, spent : 20}
	{ id : 2, nation_ref : 1, spent : 40}
}}
```

Consider the following SQL++ tuple-at-a-time query, which gives
for each nation the average number of orders per customer :

```
SELECT	n.name AS name,
		(  
			SELECT ELEMENT count(group.spent)
			FROM Customers AS c
			WHERE c.nation_ref = n.id
			GROUP BY nothing
		) AS dollar_spent
FROM 	Nations AS n;

Result :
{ name : "USA", "dollar_spent" : 60 }
{ name : "China", "dollar_spent" : null }
```

And its (almost) set-at-a-time counterpart :

```
SELECT	left.name AS name,
		right.spent AS dollar_spent
FROM 	Nations AS left
LEFT OUTER JOIN (
	SELECT	nid as id,
			count(group.spent)* AS spent
	FROM Customers as c, Nations as n
	WHERE c.nation_ref = n.id
	GROUP BY nothing
	GROUP BY n.id as nid
) as right
ON left.id = right.id;

Result :
{ name : "USA", "dollar_spent" : 60 }
{ name : "China", "dollar_spent" : missing }
```

\* : Syntactic sugar for `count(SELECT ELEMENT g.spent FROM group as g)`.

China has no customers, and `count()` returns `0` when the input list is empty (1st query) while `right.dollar_spent` is `null` if no customers are found for a given nation (2nd query).