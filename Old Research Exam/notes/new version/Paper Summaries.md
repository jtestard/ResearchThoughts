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

Describes polyglot persistence. 

## Cyclops No One Size Fits All

 - Behavioral Targeting application

Describe challenges about creating PP systems, in particular in the context of streaming engines : 
Identified by others :

 - Shivnath Babu : DBMS+ system
   - How to integrate systems into the database middleware
   - Which systems to include in the database middleware
   - Which (distributed) execution plan to pick
   - How to provision resources : adapt to unusual workload?
   - How is the data stored : coupling storage and compute systems?
   - Describe what application requirements are

Provides a good example of situation where multiple specialized systems are needed :

 - Query 1 :
   - Long slide size 
   - High arrival rate
 - Query 2 :
   - Very Short slide size 
   - Medium-High arrival rate
 - Query 3 :
   - Less short slide size 
   - Medium-High arrival rate

Experimental Results :

 - Query 1 :
   - Hadoop is the best
 - Query 2 :
   - Esper is the best
 - Query 3 :
   - Storm is the best

Database Features :

 - Query 1 :
   - slide size is long => analytical is OK.
   - High arrival rate + long slide size = lots of data. Need a horizontally scalable solution.
   - Hadoop is the best choice
 - Query 2 :
   - Very Short slide size => operational is the only option.
   - Medium-High arrival rate + short slide size = "little" data. Single node solution is OK.
   - Esper is the best choice
 - Query 3 :
   - Less short slide size => operational is the only option.
   - Medium-High arrival rate
   - Storm is the best choice


## The End of An Architectural Era (It's time for a complete rewrite)

For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database. In the Big Data era, a number of new specialized systems have emerged to meet the needs of the ever increasingly complex applications. Turing Award winner Michael Stonebreaker announced in 2006 that "the era of SQL has ended", in the sense that for any given application requirement there exists a number of new specialized systems that can beat RDBMSes to it; but there are applications whose requirements cannot be met by any single database. This led to the emergence of the so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite differing on a number of logical and architectural dimensions.

## Data Integration over NoSQL Stores using Access Path Based Mappings

 - medical and drug information application

They are building a mediator style system to integrate SQL and NoSQL stores. Their approach is to query the mediator using conjunctive SQL queries. Query is transformed into specialized system language through a mapping language called BQL. The authors use the traditional global as view approach where the queries over the views of the global schema get mapped to queries over the local schemas. However, they also store within that mapping the preferred access path (access path is akin to a query plan : which table should i be querying in the underlying sources in the presence of redundant information and NoSQL indices). Query plans are only defined/available for keys and indices of the NoSQL store. 

Once the queries are transformed to BQL, it b

## Entreprise Information Integration : Successes Challenges and Controversies

**Dina Bitton** : she explains why EII, which is a related but different problem from Polyglot Persistence, will not replace the data warehouse. In particular, EII products cannot hope to achieve the same performance as data warehousing, in part in the EII context data is virtualized (not materialized) and needs to be fetched directly from their sources, incurring an extra network overhead. EII becomes better suited for analytics of recent data while data warehousing will stay prevalent for complex analytics of historical data.

**Note** : this explains why PP system arhictecture tend to focus on one type of workload (operational or analytical), although within a workload still use multiple specialized systems.

**Mike Carey** : use EAI for updates and EII for queries.

## Max Stream

## SmartCIS

 - Application Example : smart building application.
 - What are they trying to integrate : streams and static data sources. On site sensors (physical), data from the web, machine configurations (digital). Streaming data may come from sensors or the web.
 - Integration point : single which uses SQL query language and the relational model.
 - architecture uses two run time systems (one for physical sensors and one for digital sensors). Queries are decomposed from the federated optimizer into two subqueries, one for the stream engine and one for the sensor engine.
 - Each such engine is itself an integration system which integrates purely "digital" streams and purely sensor data, respectively.

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

## Model Drive Cloud Data Storage

This paper attempts to separate the logical data model from specificities of the underlying storage applications. Provides a solution for the challenge 1 : choosing which stores to use.

## Invisible Glue : Scalable Self-Tuning Multi-Stores

- Customer Management Relationship application (CRM) example
- Large E-Commerce Example
- Traffic control example
- Does not try to provide a single data model/query language. Instead, each dataset is queried using it's native query language.
- Use a way of providing data model conversion through fragments.

Say you have a dataset D1 which you split into (possibly overlapping fragments) F1 ... Fn. You can see each fragment as a view over D1. Now say you store fragments F1...Fn into data stores S1...Sk. WOG say F1 and F2 are stored in S1. Then F1's data must be adapted to fit S1's data model. Likewise, queries over F1 from S1 must answered using S1's native query language, which means a mapping from F1's view definition and data structures in S1 must be defined. For example, if we want to allow filtering of F1 at S1 and S1 is a key-value store, then we need to install a secondary index on S1 to allow this query to happen.

Something strange in the paper is that the query language used to access data from the various data set is only defined as "the native language of the dataset". Query language are data-store specific, not data set specific, what does "native language of dataset" mean? Two possible intrepretations, equally bad :

 - The dataset is originally stored (before the decision to use estocada is made) on some data store (with its own query language). When estocada is used, the dataset is decomposed into fragments stored over various datasets but Estocada allows the user to continue to query his data using the original query language. The question becomes, what happens if the original data store wasn't the right data store to begin with and queries over the data set on that data store are too complex, then will estocada reduce that query complexity?
 - The query language being used is that of the data store on which a particular fragment is set. Then the problem is that the query language to be used becomes that of the data store currenlty storing the fragment being queried. But what if fragments are stored on multiple stores, will the user have to specify a query for each fragment? What if a fragment is migrated to a new store by Estocada, will the data on that fragment be unavailable until a query for that new store be formulated?

More on fragments and other things.

### MISO : Souping Up Big Data Query Processing with a Multi-store

This paper seems to be concerned with data movement among multi-stores in a big data system.

This system takes an existing hadoop for Big Data analytics and adds a parallel DW RDBMS to increase query performance by pushing some of the work on that system. It's an interesting, but completely different usage of multiple stores.


### Garlic IBM DB2

Shows how Garlic has been adapted as an extension to the commercial RBDMS IBM DB2.