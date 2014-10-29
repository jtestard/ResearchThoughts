EXPLAIN SELECT C.mkt_segment AS segment, count (O.order_key) AS orders
FROM Customers AS C
JOIN Orders AS O
ON C.cust_key = O.cust_key
GROUP BY C.mkt_segment;
