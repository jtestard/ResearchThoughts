## Running Example

### Finding the stores

We need an example which incorporates 3 data stores. We already have two for sure : 1) relational data warehouse CRM data, 2) mongoDB for log file of customer purchases. Our last choice must :

 - Fit in well within the CRM example
 - Break the limits of the usefulness of AsterixDB
 - Can be integrated into Forward without too many assumptions.

Two candidates :

 - Column Family stores 
 - Graph stores

Luckily, description of use cases and implementation are given in the Microsoft Data Access paper. We study them next:

#### Graph Store

We are looking for distinctive use cases that show differences betwwen a document store and a graph store in order to promote uses cases for both in an example.

Graph stores are good at performing hierachical queries such as : "who does mr. smith manages?" The equivalent SQL query would be recursive, making such a query incompatible with MySQL and MongoDB yet relevant in the CRM example.

#### Column Family Store

We are looking for distinctive use cases that show differences betwwen a document store and a column family store in order to promote uses cases for both in an example.

[TBD]

### Finding the schemas

MySQL : customer, product, sales and employee.

MongoDB : log file of customer purchases from other stores

Neo4j : employee hierarchy

### Finding the story

Take a typical CRM application for an e-commerce store, CheapShopping Inc. The CRM application uses a data warehouse to provide business owners with an interface for ad-hoc query analysis over the purchases made by their customers. It can also be used to give promotions to successful salespersons. It has the following schema :

```
Customer(id, name, address)
Employee(id, name, department)
Product(id, name, SKU, price)
Sales(id, cust_id, product_id, salesp_id, quantity_sold, order_total)
```

In this schema we show a customer bob, an employee alice, a phone and laptop product and finally sales record which show the sales of the phone and laptop to bob by alice.

The managers are well satisfied with their data warehouse, but now they have partnered with a number of e-commerce stores and have received a logs of their customer's purchases in those other stores. The log files from Amazon :

```
{ customer : "Bob", prod_name : "iPhone charger", price:"35$" }
```

and from Expedia :

```
{ ticket : { airline : "Air France", destination : "Paris", origin : "San Diego" } , customer : "bob", price : 1200 }
```

Look nothing alike, with variations on attributes, names, data types... . The in-house DBA tells the managers he just can't put those logs into the current warehouse. He tells them that a new type of schema-less database which can cope with heterogeneity and nesting is required and suggests MongoDB.

Thanks to MongoDB, the customer logs are ingested just fine, but thens comes the time to actually use the logs and runs query analysis on those logs. The managers want to know how many customers have spent more money with Amazon than using CheapShopping. This query can be formulated as follows :

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
And they realized that given the data was now located on different stores, they could not answers queries across those stores. The DBA thought about dumping the entire warehouse into MongoDB, but MongoDB notorioulsy does not handle joins!

#### Notes 

We will stop there for now : possible extra would be to add graph databases and AsterixDB into the mix.



