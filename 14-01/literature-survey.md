# Literature Survey

### Instructions
Scan the last 2-3 years of CIDR, SIGMOD, PVLDB, ICDE and see what papers have appeared (if any) on topics pertaining to running various kinds of (natively unsupported) queries and analytics on noSQL and newSQL systems.
 
 - How do you support natively unsupported data through data integration services
 - TOPICS : distributed data integration, data analytics, non-SQL systems

## List of possibly interesting papers
We have found 31 papers which are directly or indirectly to distributed data analytics and integration. Each paper is accompanied by a short description. Papers are sorted by conference and by topics.

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

