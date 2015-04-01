# Researh Exam

## Topic : Polyglot Persistence

Paper list up to now :

 - *Querying Semi Structured Data* : Serge Abiteboul (ICDT 1997)
 - *The Information Manifold* : Alon Halevy & al (S)
 - *ExSchema : Discovering and Maintaing Schemas from Polyglot Persistence Applications* : Castrejon & al (IEEE 2013)
 - *Model-Driven Cloud Data Storage* : Castrejon (CloudME 2013)
 - *Polyglot Persistence, NoSQL distilled* : Martin Fowler (2012)
 - *Building a Polyglot Solution*
 
### Pre-Analysis

To be completed when book is retrieved. Was never retrieved : will have to redo :S.



### New topics 

 - Lambda architecture : Nathan Marz
 - e

### Day 1 Friday Feb. 27th 2015

#### Uniform Access to Non Relational Databases

### Day 2 Saturday Feb. 28th 2015

### Day 3 Sunday March 1st 2015


### Polyglot Persistence, transactions and cross-database consistency

Say you have data residing on 3 databases: 

 - Shopping cart and session data on Redis (in memory only).
 - Customer Info, Product Catalog and Sales on MongoDB.
 - Recommendations on Neo4j.
 
Say you want to acknowledge a purchase, you need to :

 - put the details of the shopping cart into the order database (retrieve from Redis => store in MongoDB).
 - update the preferences of purchasing according to items of that purchase (retrieve from Redis and MongoDB, store in Neo4j).
 - delete the shopping cart from Redis.
 
It's obvious all of these items should be part of the same transaction.