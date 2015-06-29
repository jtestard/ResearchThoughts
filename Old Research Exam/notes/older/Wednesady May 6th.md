Wednesday May 6th : 

 - Come up with the clear representation of the problem.
 - Is polyglot persistnece about data integration or is it about co-design or both?
 - Make sure the motivation of the exam is clear and aligns well with the papers chosen

5-9 hours

#### Conclusions

 - *Motivation for polyglot persistence* Data sets are so different that multiple data stores are used instead of just one, because :
   1. they cannot possibly be used on the same store or
   2. They could be on the same data store, just not with the best performance.
 - Option 1 is more convincing, but option 2 can also be convincing if the performance difference is so huge that using a single data store is completely impractical.
 - 

**Restudy Motivations of each surveyed paper and figure out which problem they are trying to solve : data integration or co-design or something else.**


### Microsoft Adventure Works

PP systems are conceived before any data is present (with the exception of the legacy system integration) with the idea that given the requirements of an application and the resulting expected workloads and query/update access patterns, more than one system will be required to achieve the optimal performance and productivity*.

PP systems are implemented (in the context of web applications) using a (web) storage service approach in which each persistence interaction from an application must go through the storage service. The storage service is typically designed as a Restful API with an exposed interface which defines the way application should interact with the service. This is the architecture suggested by Martin Fowler (the man who coined the term) and Microsoft in their Data Storage for Modern High Performance Applications book.

### SOS

 - In SOS, the observation is that there is no standard for querying among the different interfaces.
 - The goal is to provide a unifying standard based on a simple API approach.
 - This allows isolation of query language specifics 
 - The use of multiple systems in the SOS interface is not justified. But all systems can use that same interface.
 - Replacing systems with other systems.
 - providing a unifying standard
 - develop applications without knowing details of various underlying systems.

Kian Win's Feedback:

 - Try to find the innovation here. For example, when considering related work for FORWARD, a simple API layer isn't enough to compare (thus this paper wouldn't be included).

#### SQL++

 - SQL++ attempts to bring a unifying standard across relational and NoSQL databases.
 - SQL++ provides configuration options.
 - SQL++ is based off SQL (not some custom API).

### Using Multiple Data Stores in the Cloud

Does not explain why polyglot persistence is motivated. Just states challenges.
