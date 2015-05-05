Hello everyone,

I came across a strange runtime results while playing around with Asterix, experimenting on query rewriting possibilities. I was trying the following AQL to run query. It is using a TPCH-like scenario with nations, customers and orders (DDL and data generator attached with this email):

```
use dataverse GlobalMarketplace;

for $n in dataset Nations
where $n.nation_key = 0
return {
  "nation_key" : $n.nation_key,
  "nation_name" : $n.nation_name,
  "aggregates" : (
     for $o in dataset Orders
     for $c in dataset Customers
     where $o.cust_ref = $c.cust_key and $c.nation_ref = $n.nation_key
     let $group := { "o" : $o, "c" : $c, "n" : $n } 
     group by $order_year := $o.order_year with $group
     order by $order_year desc
     limit 3
     return {
        "order_year" : $order_year,
        "list_price" : sql-sum(for $g in $group return $g.o.total_price)
     }
  )
}
```

It gives me the output that I expect, but has strange time characteristics. I have done a few experiments with different sizes for the customers and orders datasets (full experiments available [here](https://docs.google.com/a/eng.ucsd.edu/spreadsheets/d/1FoHroij7HftomI488hI3tHVogK6vbAUVq3ZVhR37i6g/edit#gid=0)), and increase the number of orders from 110 000 to 120 000 increase the runtime from 265ms to 11sec (almost 1000x slower)! I have checked, the query plans for both queries are identical. 

For those interested, here is the query's SQL++ equivalent :

```
use dataverse GlobalMarketplace;

SELECT  n.nation_key as nation_key,
        n.nation_name as nation_name,
        (
          SELECT  order_year as order_year,
                  sql-sum(o.total_price) as list_price
          FROM  Orders as o,
                Customers as c
          WHERE o.cust_ref = c.cust_key and
                c.nation_ref = n.nation_key
          GROUP BY o.order_year as order_year
          ORDER BY order_year DESC
          LIMIT   3
        ) as aggregates
FROM Nations as n;
```