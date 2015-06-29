### Running Example for the Research Exam

First running example was taken from Martin Fowler's article, but it wasn't convincing enough for the audience because while it showed a use of multiple stores, it did not provide a strong enough argument that the use of multiple stores was necessary.

The running example must motivate the problem of polyglot persistence. The polyglot persistence problem is motivated when :

 - application requirements are not met by any single database (fuzzy)
 - Capability mismatch : queries require special operators/functions that aren't all available on any given single database.
 - Data Model mismatch : data required by the application does not fit a single data model (data-specific problem).
 - Performance mismatch : adequate performance for all queries over the data is not met by any given single database because of one of the following problems (performance-specific problem) :
   - The data being stored does not fit the data model of the database being used and queries over this data are more complicated because of this data model mismatch (e.g. storing a graph in an RDBMS and asking a graph-related query in SQL).
   - The queries over the database have different runtime and consistency requirements (Very fast, simple BASE queries are asked alongside with more complex ACID transactions).
   - The volume of data being queried varies significanlty across queries and the best system (single node realtime vs distributed realtime vs distributed batch) to answer each query is different (Babu's example).
   - The 

 - *Motivation for polyglot persistence* Data sets are so different that multiple data stores are used instead of just one, because :
   1. they cannot possibly be used on the same store or
   2. They could be on the same data store, just not with the best performance.
 - Option 1 is more convincing, but option 2 can also be convincing if the performance difference is so huge that using a single data store is completely impractical.



### Exisiting Running Exmaples

 - CRM with extra social network graph and log files (Invisible Glue)
 - Open Data Warehousing for Cities (Invisible Glue)
 - Large Scale E-commerce application (Invisible Glue)
 - Behavioural Targeting (DBMS+)
 - Cure & al (Medical Data)
 - SOS (
 - 