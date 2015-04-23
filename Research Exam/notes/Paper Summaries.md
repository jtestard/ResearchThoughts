## An XML Query Engine for Network Bound Data

Authors have realized that XML has become a globalized standard for data exchange among heterogeneous sources. Therefore, it becomes practical for them to build a system, in this case called Tukwila, which focuses on integrating network-bound* XML data sources.

\* : Network-bound data sources are only available through a network and can only be obtained through reading and parsing XML streams.

 - query focus : XQuery queries.
 - location of data : network
 - source type : supports XML interface.
 - handles updates : no
 - data format : XML
 - data streams : yes
 - data size : up to ~100MB XML files

## Query Optimization over Web Services

Authors realized that Web Services are becoming an increasingly popular way to share data and that there were no managements systems for Web Services with decent query optimizers. Therefore, they came up with the Web Service Management System (WSMS), which does exactly that.

Moreover, the authors have made several realizations that made several web-service specific query optimizations possible. First, that the performance of a pipelined plan over web services is dictated by the slowest web service in the pipeline. Second, thath the optimal arrangement of web services in the pipeline depends only on response times. This allows them to find a polynomial time algorithm to find the optimal plan (my guess is the algorithm is greedy) even in the presence of precedence constraints.

 - query focus : SPJ
 - location of data : network
 - source type : web service
 - handles updates : no
 - data format : XML
 - data streams : chunks (so yes, kind of).
 - data size : doesn't say

## Query Processing in the AquaLogic Data Services Platform

## Garlic

## MySQL Pluggable Storage Engine Architecture

## Martin Fowler

## Cyclops No One Size Fits All

## The End of An Architectural Era (It's time for a complete rewrite)

For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database. In the Big Data era, a number of new specialized systems have emerged to meet the needs of the ever increasingly complex applications. Turing Award winner Michael Stonebreaker announced in 2006 that "the era of SQL has ended", in the sense that for any given application requirement there exists a number of new specialized systems that can beat RDBMSes to it; but there are applications whose requirements cannot be met by any single database. This led to the emergence of the so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite differing on a number of logical and architectural dimensions.

## Data Integration over NoSQL Stores using Access Path Based Mappings

They are building a mediator style system to integrate SQL and NoSQL stores. Their approach is to query the mediator using conjunctive SQL queries. Query is transformed into specialized system language through a mapping language called BQL. The authors use the traditional global as view approach where the queries over the views of the global schema get mapped to queries over the local schemas. However, they also store within that mapping the preferred access path (access path is akin to a query plan : which table should i be querying in the underlying sources in the presence of redundant information and NoSQL indices). Query plans are only defined/available for keys and indices of the NoSQL store. 

Once the queries are transformed to BQL, it b

## Entreprise Information Integration : Successes Challenges and Controversies

**Dina Bitton** : she explains why EII, which is a related but different problem from Polyglot Persistence, will not replace the data warehouse. In particular, EII products cannot hope to achieve the same performance as data warehousing, in part in the EII context data is virtualized (not materialized) and needs to be fetched directly from their sources, incurring an extra network overhead. EII becomes better suited for analytics of recent data while data warehousing will stay prevalent for complex analytics of historical data.

**Note** : this explains why PP system arhictecture tend to focus on one type of workload (operational or analytical), although within a workload still use multiple specialized systems.

**Mike Carey** : use EAI for updates and EII for queries.

## Max Stream

## SmartCIS

## Nathan Marz : Lambda Architecture

## Usign Mulitple Data Stores in the Cloud : Challenges and Solutions

These guys make a survey of uses cases for using multiple data stores in the cloud. They divide their survey into 2 categories :

 - Multiple applications sharing a specialized system
 - One application using multiple specialized systems

The latter part of the survey is of obvious interest to us. Their conclusions corroborates my opinion, that is their is a wide variety of challenges involving PP, but existing solution only target a subset of each.

Will have to reference the grid they show on page 96, because our project will have a similar one.

## ODBAPI : A unified REST API for relational and NoSQL stores

Provides a unifying REST API to talk to multiple specialized systems (key-value, document and relational stores). Lacks a declarative query language and any expressiveness beyond simple key retrieval (no joins, group bys...).  Does not provide any transactional guarantees. 

Note : StoneBreaker outlines the problems about using NoSQL databases and their heterogeneous APIs. StoneBreaker on NoSQL and entreprises.