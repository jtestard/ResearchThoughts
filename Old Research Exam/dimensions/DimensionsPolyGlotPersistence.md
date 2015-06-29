# Dimensions for PolyGlot Persistence

What if we limited ourselves to :

 - PP systems focusing on performance
 - Analytical processing (we forget about OLTP)

## Problems

 - Different components of an application fit the features of different database systems.

Each paper that follows shows an example of an application requirements and the corresponding required features.
 
##### *No One Size Fits All* (Babu)

Requirements :

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

##### *Polyglot Persistence* (Martin Fowler) : 

Requirements :

 - Query 1 :
   - Retrieve Session Data and Shopping cart.
   - Very fast/frequent retrieval required
 - Query 2 :
   - Recommend products to customers based on their friends.
   - products have no relationships but are expected to have an evolving schema.
   - friends are part of a social network.
 - Query 3 :
   - Want to search products instantly.
   - Very fast/frequent search
 - Query 4:
   - Want to order payment and product shipment/inventory with strong consistency.

Database Features :

  - Query 1 :
    - High availability and simple key-value retrieval is sufficient => key-value store
  - Query 2 :
    - Products should be in a document store.
    - Friends should be in a graph store.
  - Query 3 :
    - A search engine such as Elastic Search
  - Query 4 :
    - Strong consistency guarantees.
    - A relational database.

## Systems

 - Martin Fowler's e-commerce platform.
 - Microsoft Highly Available Data Access Adventure Works
 - Shivnath Babu's cyclops

## Techniques

 - Multiple Databases

## Results


## Issues

The features of database systems have different dimensions :

 - Data model and query capabilities:
   - Search engine 
   - Key-Value Store
   - Document Store
   - Extensible Record Store
   - Graph Store
   - Relational
 - Persistence
   - persisted, retrievable data
   - data streams
 - Scalability
   - Single Machine - Vertical Scaling
   - Horizontal Scaling
 - Storage 
   - Main-memory
   - SSD storage
   - Hard Disk
 - Workload
   - Operational
   - Analytical
 - System Type 
   - Batch
   - Realtime
 - Data Partitioning
   - sharding
   - replication
 - CAP Theorem compromise
   - CP
   - CA
   - AP 

Application Requirements :

 - wewe