```
SELECT   n.nation_key as nation_key,
    n.nation_name as nation_name,
    (
    	WITH price_per_year AS (
    		SELECT	o.order_year AS order_year,
    				sql-sum (
						SELECT ELEMENT g.o.total_price
						FROM group as g
					) AS list_price
			FROM	Orders as o,
					Customers as c
			WHERE	o.cust_ref = c.cust_key and
   		   			c.nation_ref = n.nation_key
   		   	GROUP BY o.order_year as order_year
    	)
		SELECT	ppy.order_year as order_year,
				ppy.list_price as list_price
		FROM   price_per_year as ppy
		ORDER BY  ppy.price_per_year DESC
		LIMIT  3
    ) as aggregates
FROM Nations as n;
```

```
SELECT   n.nation_key as nation_key,
    n.nation_name as nation_name,
    (
		SELECT	order_year as order_year,
				list_price as list_price
		FROM	Orders as o,
				Customers as c
		WHERE	o.cust_ref = c.cust_key and
				c.nation_ref = n.nation_key
		GROUP BY o.order_year as order_year
		LET		list_price := sql-sum (
					SELECT ELEMENT g.o.total_price
					FROM group as g
   		        )
		ORDER BY list_price DESC
		LIMIT  3
    ) as aggregates
FROM Nations as n;
```

We choose `WITH` because it is easier to implement (although not as flexible) than let (and backwards SQL compatible). We have only allowed so far one `WITH` statement per subquery. **TODO** : extend this feature to allow `WITH` statement with multiple assignments.

