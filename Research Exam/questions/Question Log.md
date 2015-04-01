## Question Log

**Question** : In Alon Halevy's survey on answering queries using views, the problem in the data integration contents was that it was impossible to obtain an equivalent rewriting of a SQL query Q using views V1 ... Vn, and one had to settle for a *maximal* rewriting. How is this expressed formally?

**Answer**: Using containment of queries.
___

**Question**: What is the difference between local-as-view and global-as-view approaches in data integration?

**Answer**: Both approaches deal with modeling external sources in an aggregator system (the mediator) which combines the data from all those sources and makes them available in one place. To simplify the answer, lets consider that all those sources contain data represented conceptually in relational tables.

The *Global-As-View* approach provides on the mediator a set of views made from those tables which end-users can query. When a new source is added to the system, views have to be updated to take the new source's data into account.

On the other hand, the *Local-As-View* approach takes a global (or mediated) schema and considers that each source contains some small piece of the global schema's data (a view over the global schema). When a new source is added to the system, tables from the new sources have to be expressed in terms of the global schema.

**Follow-Up Question**: Is FORWARD Global-As-View or Local-As-View (from the [FORWARD website's description](http://forward.ucsd.edu/architecture.html)?

FORWARD is clearly Global-As-View. FORWARD's grandfather is Garlic, which was also a Global-As-View system.
___

**Question**: What are the differences/similarities between the challenges of the 1990's integration systems and the 2010's polyglot persistence problem?

**Answer**:The initial systems were interested in providing a uniform query interface for *locating* data sources, *extracting* each source individually and *combining* the results. The aim was to make such a process feasible and provide the most accurate response given the large (and possibly varying) number of sources each with their own dataset and varying degrees of query capabilities.

The polyglot persistence problem is based on the premise that there is no single system which is effective when considering all types of data access, therefore multiple systems should be used in coordination to make all types of data access requirements of a given application feasible and performant. 
___

**Question**: In order to provide a uniform query interface, developers currently use a software development pattern called the *Repository Pattern*. What is this pattern?

**Answer**: In the Repository Pattern, an application centralizes all of its persistence storage and retrieval through a *Repository Module*. The Repository Module is not only responsible for storing and retrieving objects, but also ensuring properties about data such as integrity constraints. In order to guarantee that some constraints are satisfied, it may have to ensure atomicity and isolation for the transaction that require it, if the underlying data store does not already provide them.

The repository must be specify how the database(s) should be queried through the use of an API. These queries can be understood as views over the database. Given repository modules are application-specific, a new repository module has to be built for each application. 