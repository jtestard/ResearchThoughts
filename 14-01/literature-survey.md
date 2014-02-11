# Literature Survey

### Instructions
Scan the last 2-3 years of CIDR, SIGMOD, PVLDB, ICDE and see what papers have appeared (if any) on topics pertaining to running various kinds of (natively unsupported) queries and analytics on noSQL and newSQL systems.
 
 - How do you support natively unsupported data through data integration services
 - TOPICS : distributed data integration, data analytics, non-SQL systems

## List of possibly interesting papers
We have found 31 papers which are directly or indirectly to distributed data analytics and integration. Each paper is accompanied by a short description. Papers are sorted by conference and by topics.

 - The canonical example from which other papers are compared is the 2011 CIDR Forward paper.
 - The canonical objective is to produce an interface to supported natively unsupported queries or analytics which may come from various, heterogeneous sources. 
 - Not all papers shown here share this objective
 - Some papers, such as *How Achaeans Would Construct Columns in Troy*, attempt to implement unsupported functionality in existing systems in order to answer natively unsupported queries.
 - Some papers describe help achieve a subset of the canonical objective, for instance *Data Curation at Scale: The Data Tamer System*.
 - Some papers do not attempt to produce an interface to query data on heterogeneous source but might provide some insight.
 
### CIDR 2011
<!--- 
- *Data Consistency Properties and the Trade-offs in Commercial Cloud Storages: the Consumer's Perspective* : this paper investigates consistency guarantees vs performance offerings across several NoSQL platforms (Amazon SimpleDB, Microsoft Azure Table Storage, Google App Engine datastore, and Cassandra). 
  *Ibis: A Provenance Manager for Multi-Layer Systems* : this paper describes a provenance manager which integrates metadata from heterogeneous sources. The manager handles integration of provenances with varying levels of granularity through a formal model described in the paper.
---> 
    
 - *Deuteronomy: Transaction Support for Cloud Data* : this papers describes how to decompose functions from the database engine kernel into two components.
   - The transactional component (TC) : manage transactions (concurrency control,undo/redo,...) without knowledge of physical location. 
   - The data component (DC) : maintain data cache and uses wrapper-like access methods without knowledge of transactions.
   This decomposition allows to transcend the location of data. It also guarantees ACID properties.
 - *The SQL-based All-Declarative FORWARD Web Application Development Framework*
 - *Here are my Data Files. Here are my Queries. Where are my Results?* : paper describe how to create systems for querying raw datafiles, without any extra information (schema,data storage format...). The system incrementally provides its own environment given the queries. As such, natively unsupported queries are handled by incrementally changing the system environment.   

### CIDR 2013
 - *How Achaeans Would Construct Columns in Troy* : this papers describes how to implement column store functionality in relational database systems.  
 - *Data Curation at Scale: The Data Tamer System* : this papers describes how to integrate a new data source and semantically integrating it.

<!--- 
- *Data Integration and Data Exchange: It's Really About Time* : time-aware data integration of multiple sources concerned by one entity. 
---> 

### ICDE 2011
<!--- 
 - Distributed Cube Materialization on Holistic Measures 
 - ES2: A Cloud Data Storage System for Supporting Both OLTP and OLAP
--->
 
 - *Extensibility and Data Sharing in Evolving Multi-Tenant Databases* : this paper describes to handle data from heterogeneous sources within a relational database.

### ICDE 2012
 - *Automatic Extraction of Structured Web Data with Domain Knowledge* : this paper focuses more on data extraction then querying, but 

### ICDE 2013
 - Interval Indexing and Querying on Key-Value Cloud Stores
 - Automating Pattern Discovery for Rule Based Data Standardization Systems

### SIGMOD 2011
 - Joint Unsupervised Structure Discovery and Information Extraction

### SIGMOD 2012
 - NoDB: Efficient Query Execution on Raw Data Files
 - Holistic Optimization by Prefetching Query Results

### SIGMOD 2013
 - Inter-Media Hashing for Large-scale Retrieval from Heterogeneous Data Sources

### VLDB 2011
 - Albatross: Lightweight Elasticity in Shared Storage Databases for the Cloud using Live Data Migration
 - Automatic Wrappers for Large Scale Web Extraction
 - Citrusleaf: A Real-Time NoSQL DB which Preserves ACID
 - OXPath: A Language for Scalable, Memory-efficient Data Extraction from Web Applications
 - HYRISE—A Main Memory Hybrid Storage Engine
 - PathSim: Meta Path-Based Top-K Similarity Search in Heterogeneous Information Networks

### VLDB 2012
 - hStorage-DB: Heterogeneity-aware Data Management to Exploit the Full Capability of Hybrid Storage Systems
 - Querying Schemas With Access Restrictions
 - Relation Strength-Aware Clustering of Heterogeneous Information Networks with Incomplete Attributes

### VLDB 2013
 - Big Data Integration
 - Towards Database Virtualization for Database as a Service
 - Scalable Transactions across Heterogeneous NoSQL Key-Value Data Stores
 - Online Ordering of Overlapping Data Sources
 - Microsoft SQL Server’s Integrated Database Approach for Modern Applications and Hardware

#### First circle
 - The SQL-based All-Declarative FORWARD Framework [CIDR 2011]
 - Scalable transactions across heterogeneous Key-value Data stores [VLDB 2013]
 - Materializing SQL queries in key-value stores [SIGMOD 2014]

#### Second circle 
 - How Achaeans Would Construct Columns in Troy [CIDR 2013]
 - Holistic Optimization by Prefetching results [SIGMOD 2012]
 - CitrusLeaf: Real-time NOSQL DB which Preserves ACID [VLDB 2011]
 - Microsoft SQL Server's Integrated Database Approach to Modern Applications and Hardware [VLDB 2013]

We should first look at the four articles of the first circle and investigate how these different articles can be compared :
 - what are there goals (problems they are trying to solve), 
 - what is their angle to tackle the problem.
 - how do the goals relate to each other.

Then, pick certain criteria and classify each framework according to that criteria. 

#### Holistic Data Access Optimization for analytics report
 - In the previous paper, we develop a framework and language to help the developer focus on the logic of his application and minimize the plumbing code he is required to do. 
 - Following this, we also want to extend that framework in order to optimize the queries (including analytical queries) the developer writes in that language.
 - This is why we develop the Forward Query Optimizer called Collage.
 - This optimizer integrates data from multiple heterogeneous sources which the developer specified, and finds an optimal way to execute that query using :
   - set-at-a-time semantics
   	- denormalized and normalized sets
   	- performance using normalized sets is highly superior.
 - We integrate external objects without requiring an explicit mapping.
   - we integrate SQL, JSON and java sources. We extend our integration using wrappers.
   - we provide optimality given a set of sources and its query capabilities (we wish to do so).
 
#### Scalable Transactions across Heterogeneous NoSQL Key-Value Data Stores
 - How to implement multi-item transactions (atomic, safe, reversible data state changes) in heterogeneous systems (data stores with heterogeneous formats).
 - The author explores existing solutions of how to implement mutli titem ACID transactions using cloud / NoSQL systems.
   - application layer manages transactions : programmer error prone.
   - implement transaction support in the data source : may limit scalability/availability.
   - use a middleware to coordinate transactions : may work, but only in controlled environment (according to author).
 - The author defines a new solution : create a transaction protocol shared by data sources and add a transaction API layer on top of each data source.
   - communication between data stores will have to use this protocol.

#### Materializing SQL Queries in Key-Value Stores
 - 	 
 - For details about features of different flavors of key-values stores see Cartell's survey (SIGMOD record).
 - We have examples of applications which need the high performance insertion/look up provided by key value stores but also need an "online view" of the data managed by the system.
   - application performance manager (APM) : monitors performance of an enterprise system, requires a huge number of insertions (from different components of the system) and at the same time requires heavy analytics processing.
   - Smart traffic manager (STM) : traffic management on roads an highways. Data comes from sensors such as cameras, loop detectors, smartphone geolocalization... this data has to be inserted at a very fast rate. Using materialized views data can be accessed fast in any format.
 - Our solution is to continue using key-value store as data storage for these types of applications, but use materialized views to do the analytics processing.
 - We benefit from the consisteny guarantees provided by the SQL materialized views while keeping the scalability and availability advantages of NoSQL sources.x  

#### Microsoft SQL Server's integrated database approach for modern applications and hardware
 - We want to build a modern database fit for the modern usage we have of data :
   - store huge amounts of data
   - maximize consistency for queries through transaction processing
   - process huge amounts of data for analytics processing
 - According to the author, different types of storage are preferred for each task :
   - transaction processing : main memory focused row store
   - analytics processing : column store
   - mixed approach for queries that cannot be seperated
 - Both types of storage are integrated in a single database.

#### Holistic Optimization by Prefetching results
 - We want to optimize performance of database/web service backed applications by prefetching query results.
 - Prefetching allows to start a query process before the results of the query are actually required in order to have the results readily available when the user needs them, without having to wait for them to arrive. This can greatly reduce latency in application which need to access remote data located on databases/web services.
 - Problems may occur :
   - Prefetches may be wasted and uses bandwith and computing power for nothing
 - Up to now, prefetching has had limited value, because :
   - it was limited to query access patterns, and often resulted in unnecessary prefetches.
   - another approach was to analyze the program which would access the database in order to automatically insert the prefetch requests. The problem is that the use case of current applications such as web services, such program analysis cannot be done?
 - We offer a solution which is applicable to called procedures(?) and avoids wasteful prefetches.
 - Examples of query prefetching opportunities :
 - The tool we develop rewrites java programs to integrate prefetching requests
 - Background
   - Prefetch Execution Model
     - Cache keyed by tuple
     - Control Flow Graph and Call Graph (for control flow analysis)
 - Query Anticipability
   - We use a technique called *anticipable expressions analysis* and use it to compute query anticipability, in other words : can we know for sure that this query will be called?
   

#### How Achaeans would construct columns in Troy
 - Implement column store functionality in row-store DBMS without :
   - requiring to change the source code (or even see it)
   - hindering performance for complex queries (such as analytical queries)
   - requiring different storage systems for different storing formats
 - The author suggest the use of UDFs (User Defined Functions) to do the job :
   - UDF can be used to enable column store functionality in an existing row store
   - UDF syntax is very similar between most types of DBMS
   - UDF functions can be optimized state-of-the-art query optimizers.
 - Problems :
   - User queries need to be (slightly) rewritten in order to use the UDF for data access.
   

#### Citrusleaf : Real-time NoSQL DB which preserves ACID 
 - NoSQL distributed database with ACID properties and immediate consistency.
 - 