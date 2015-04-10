#### More on Difference between the GAV mediators and PP systems

GAV mediators were built with the intention of aggregating data originally from different sources into a centralized location and make it available for querying (and possibly updating) from that location under a common format.

PP systems are conceived before any data is present (with the exception of the legacy system integration) with the idea that given the requirements of an application and the resulting expected workloads and query/update access patterns, more than one system will be required to achieve the optimal performance and productivity*.

PP systems tend to be implemented (in the context of web applications) using a (web) storage service approach in which each persistence interaction from an application must go through the storage service. The storage service is typically designed as a Restful API with an exposed interface which defines the way application should interact with the service. This is the architecture suggested by Martin Fowler (the man who coined the term) and Microsoft in their *Data Storage for Modern High Performance Applications* book.

### Similarities

Such an architecture can benefit from a GAV system approach in the sense that the restful API can be understood as a set of views over the mutliple "one size" systems.

### Differences


#### Updates

**Need to verify** The big difference is that PP systems expect the restful API to be the main way that data on the storage systems gets updated while on typical GAV mediators, each data source is expected to be updated independently and the mediator is only responsible of ensuring that when changes happen its views are updated accordingly. 

==> Verification : 
#### d

-----------

\* : productivity is obtained (at least) from a unifying query language and semantic compensation from discrepancies.



## Web Service and GAV Mediator Hypothesis

The Web Service (and Repository Pattern) used for Polyglot Persistence in the industry. 
Once the choice is made that the application requires multiple coordinating data stores, it is the "standard" way to approach integration of multiple 

is nothing more than a manifestation of a Global-As-View mediator approach in a slightly different context from the 1990's.


 - Functions in repository pattern -> Views in GAV mediator.
 - Multiple databases with different query semantics ->
 - Updating the multiple database -> incremental view maintenance.

 
Need to verify :

#### Understand completely the two systems we want to show the equivalence for

 - Make sure exisiting definition of repository pattern is exhaustive.
 - Understanding how GAV systems update and retrieve data. Focus on correctness, performance does not matter for the moment

### w

 - Show that any retrieve function exposed by the repository module is is equivalent to a GAV view.
 - Show that the update function exposed by the repository module is equivalent to an update of a GAV view
