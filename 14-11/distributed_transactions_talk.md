# Distributed Transactions talk 

### Content

Describe transactions in two slides : 

### Transactions

#### 1) Transactions (in traditional RDBMS )

Goal : 

 - atomicity : a transaction may contain multiple operations. All of them should happen or all of them shouldn't happen (no inbetween).
 - consistency : the successful or failed execution of a transaction should leave the database in a consistent state.
 - isolation : mulitple transactions should be correctly processed simultaneously.
 - durability : in case of sudden crash of the system, the system should recover in a way which satisfies consistency. 

Techniques to achieve the goal : 



- Locking protocols (isolation, consistency)
- Rollback mechanisms (consistency)
- Recovery mechanisms (durability)
 
- Two phase commits : (atomicity)
  - ensure updates happen atomically on multiple database systems.

#### 2) Cloud-based data services

Definition :

Cloud storage is a model of data storage where the digital data is stored in logical pools, the physical storage spans multiple servers (and often locations), and the physical environment is typically owned and managed by a hosting company.


Goals : 

 - availability : services should be available, even in case of partial hardware failure.
 - scalability : services should be able to handle variations in request load.
 - responsiveness : services should respond to user requests with minimum delay.

Techniques :

 - Data replication
 - Horizontal scaling
 - Elastic scaling
 - Simpler data/query models:
    - Key value stores

#### 3) Transactions in the cloud

 - Data partitioning
 - Transactions over multiple partitions
 - Multi-row transactions
 
. Wei, G. Pierre, and C.-H. Chi. Scalable Transactions forWeb Applications in the Cloud. In Proceedings of theEuro-Par Conference on Parallel Processing, 2009

We should classify methodologies used in the cloud to tackle each one of these problems.
Would be useful to classify systems according to their characteristics.  

### The CAP theorem

Can only have two of the following happening together at any given time :

 - Consistency
 - Availability
 - Partition tolerance (distribution)

Why is that?

 -> Refer to evenutal consistency paper.

### Eventual consistency

### Design Proposals

 - Unbundling transactions in the cloud
 - Chubby/Paxos
 - Building a Database on S3
 
### System proposals

 - CloudTPS
 - G-Store
 - Elastras
 - Azure Database
 - H-Store
 - Google Megastore
 - ec-Stre



### Features

### Feature support



Fundamental approaches :

 - CloudTPS
 - ElasTras
 - G store

Response approaches

 - deuteronomy
 - heterogeneous KV stores
 
### End notes

 - We do not look at performance.



### Paper description

#### CloudTPS 2011

 - They try to solve the problems of web applications which require ACID properties and scalability to work properly.
 - Their solution is to add a transaction management layer on top of existing scalable database services (which by themselves only provide weak consistency) to provide Isolation and Atomicity.
 - The use of a centralized transaction layer would not be scalable. Therefore, they split the transaction management layer into local transactions managers (LTMs) and partition the load of transaction processing across them.
 - Target applications : payment services, online auctions.
 - Transactions are guaranteed only on key-value pairs.
 - They rely on single item transaction 
 - Properties of web services transactions :
   - They are short lived (encapsulated into a user request).
   - They only access a fairly small, well-defined set of data items. This implies low amount of conflicts between transactions.
   - Read-only transactions can often produce useful result by accessing an older, yet consistent version of the data accessed.

#### G-Store 2010

- Target applications : Online gaming, social networks, collaborative editing
- Opposed to CloudTPS in the sense that they focus on multi-key transactions.
- Concept of a *keyGroup* which defines the set of keys on which the transaction is based.

## Sections

### Target problems

The *Eventually Consistent* paper proposes a classification of consistency models present in distributed data storage.

### In-Memory 

 - Scalaris
 - H-Store

### Fundamentals

 - Eventually consistent
 
### Key-value transactions

 - CloudTPS

### Trunk

### Branches

## Papers

 - *Adapting Microsoft SQL Server  for Cloud Computing* : mid value
 - *An Evaluation of Alternative Architectures for Transaction Processing in the Cloud-kossman* : high value (probably)
 - *G-store: a scalable data store for transactional multi key access in the cloud* : good to high value
 - *CloudTPS- Scalable Transactions for Web Applications in the Cloud* : high value
 - *Deuteronomy- Transaction Support for Cloud Data* : high value
 - *Don’t Settle for Eventual- Scalable Causal Consistency for Wide-Area Storage with COPS*
 - *Unbundling Transaction Services in the Cloud* : high value
 - *elastras* : high value
 - *final_hstore* : old, few links to other works.
 - *Hyder – A Transactional Record Manager for Shared Flash* : not sure of relevance.
 - *ocking Key Ranges with Unbundled Transaction Services* : good value
 - *Towards Elastic Transactional Cloud Storage with Range Query Support* : high value.
 - *Building a database on S3* 
 - *Sinfonia*
 - *Azure Cloud Database*

### Microsoft Academic Search Rank

#### Keywords : transactions + cloud
 - *Towards elastic transactional cloud storage with range query support* (#2)
 - *Deuteronomy: Transaction Support for Cloud Data* (#3)
 - *Scalable Transactions for Web Applications in the Cloud*
 - *Elastras*

### Industry software
 - *Dynamo: Amazon’s highly available key-value store. In Proceedings of the 21st ACM Symposium on Operating System Principles*
 - *Pnuts: Yahoo!’s hosted data serving platform*
 - *Bigtable: A Distributed Storage System for Structured Data*
 - *Redis: an open-source advanced key-value store* (~mild)


### Fundamentals 

 - *M. T. Ozsu and P. Valduriez, Principles of distributed database systems, 2nd ed. Prentice-Hall, Inc., Feb. 1999.*
 - *E.A.Brewer.(InvitedTalk)Towards Robust Distributed Systems.In Proc. of PODC, page 7, 2000*
 - *Principles of Transaction Processing, Second Edition, Morgan Kaufmann, 2009*
 - *Concurrency Control and Recovery in Database Systems.*

### Benchmarks

 - *M.J. Carey,D.J. DeWitt, and J.F. Naughton.The007Benchmark. In Proc. of SIGMOD, pages 12–21, 1993*
 - *TPC-C Benchmark, Transaction Processing Performance Council, www.tpc.org*
 - *TPC benchmark E standard specification version 1.9.0.*
 - *TPC-W 1.8 Benchmark, Transaction Processing Performance Council, www.tpc.org*
 - *Benchmarking cloud serving systems with YCSB. In Proceedings of the 1st ACM Symposium on Cloud Computing. ACM, New York, NY, 143–154*

 
### Notes Flash vs SSD

- Flash is the technology used by modern SSDs to achieve a non-volatile state.
- DynamoDB vs SimpleDB:
  - simpleDB is harder to scale but more flexible in terms of query capabilities.
  - dynamoDB scales seemlessly but has very limited query capabilities.