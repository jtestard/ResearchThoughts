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
 - hStorage-DB : Heterogeneity-aware Data Management to Exploit the full capability of Hybrid Storage Systems [VLDB 2012]
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

#### The SQL-based All-Declarative FORWARD Framework
 - Problem :
   - Database-driven Web Applications need a lot of plumbing code to be written even for a small amount of business logic.
   - The state of the application has to be maintained across the three application layers :
     - visual layer
     - application logic layer
     - database layer
   - Each layer uses different languages, plumbing code is required to transform data objects from one representation to another in order to transfer data from one layer to the other.
   - Modern web applications which use AJAX need specific plumbing code for each user interaction and on each layer.
 - Are we capable of making the developer's life easier by automating of all of this predictable, logic-independent plumbing code?
 - Solution : 
   - Yes, through the use of SQL++, a variant of SQL, we only require the developer to define the logic of his application and we take care of all the plumbing code.
   - By logic, we mean :
     - what is the data? relational=(table name, schema)
     - where it is located ? Main memory session, SQL databse, commercial web-service (facebook api, google api...), NoSQL key-value store...
     - what logical operations should be applied to the data?
     - where it should be displayed
   - single language access

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
 
#### H-StorageDB : Heterogeneity-aware Data Management to Exploit the Full Capability of Hybrid Storage Systems
 - We do not know how to use properly heterogeneous storage systems.
 - We do a lot of things with heterogeneous systems sub-optimally even after a lot of human effort has been put in.
 - We do not try to change our heterogeneous system to a homogeneous one. Instead we want to take advantage of the capabilities of each storage device.
 - We have a framework designed for heterogeneous storage management, called hStorageDB.   
 - Using this framework, we can collect and use semantic information that is otherwise unavailable yet very important for the management of a heterogeneous system.
 - We have some performance analysis. Substantial
 - The heterogeneity mentioned in this paper is the heterogeneity of storage devices available to a database system, not the heterogeneity of data sources format and/or query capabilities.
 - The problem is fundamentally different, and a way of mapping this problem to our problem remains to be examined. 

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

#### How Achaeans would construct columns in Troy

#### Citrusleaf : Real-time NoSQL DB which preserves ACID 