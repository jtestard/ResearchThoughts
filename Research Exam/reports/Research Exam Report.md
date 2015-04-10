# Research Exam Report

### Goals

Our goals are to :

 1. Describe why the polyglot persistence problems has emerged.
 - Describe why the polyglot persistence problem matters.
 - Define formally the polyglot persistence problem.
 - Describe the challenges the polyglot persistence problem creates.
 - For each challenge, describe the solutions found so far if they exist. If more than one solution exist for any given problems, compare the tradeoffs between solutions.

There are some parallels between use cases and challenges. Not all uses cases care most about the same challenges : for example adaptive stream QP does not care so much about inter-database integrity. 
 

##### Note to self

Do not restrict yourself to systems which explicitly consider polyglot persistence as a goal. PP is a very new problem and such systems are very few in numbers. Rather, consider the challenge dimensions individually and compare any solution to them (old or new).

#### Repository Pattern and Global as View Mediators

##### Hypothesis

The Repository Pattern used for Polyglot Persistence in the industry is nothing more than a manifestation of a Global-As-View mediator approach.

 - Functions in repository pattern -> Views in GAV mediator.
 - Multiple databases with different query semantics ->
 - 

### Introduction

Different currents have tackled the problem at different times

 - Data Integration Systems from the 1990's
 	- Information Manifold
 	- Garlic
 	- Alon Halevy's survey
 - Query Optimization for 1990's systems
 - Stream processing adaptability
   - Shivnath Babu's survey
   - Lambda Architecture
 - Capability enhancement of existing applications
   - Chris Richardson's "indices" : "increase" capabilities of key-value stores.
   - ExSchema : add schemas to NoSQL apps
   - Support Schemaless RDBMS
 - Uniform Access to NoSQL heterogeneous query processing systems
   - SOS platform
   - Forward

### Survey and challenges papers


##### Answering Queries using Views (Alon Halevy)


##### No One Size Fits (Shivnath Babu)

The DBMS+ Research Agenda :

 1. How to integrate systems into a DBMS+?
   - Federated approach
   - Imperial approach
 2. 


### Data Integration Systems from the 1990's

The initial systems were interested in providing a uniform query interface for *locating* data sources, *extracting* each source individually and *combining* the results. The aim was to make such a process **feasible** and provide the most accurate response given the large (and possibly varying) number of sources each with their own dataset and varying degrees of query capabilities.

The polyglot persistence problem is based on the premise that there is no single system which is effective when considering all types of data access, therefore multiple systems should be used in coordination to make all types of data access requirements of a given application feasible and performant. We call an application whose requirements cannot be met by any single storage system a polyglot persistence application.

In Alon Halevy's survey on answering queries using views, the problem in the data integration contents was that it was impossible to obtain an equivalent rewriting of a SQL query Q using views V1 ... Vn, and one had to settle for a *maximal* rewriting.

##### Systems

 - Information Manifold
 - Garlic
 - TSIMMIS

##### Optimization

 - TSIMMIS

#### Stream 

Suggestion : compare data integration systems from a Polyglot persistence perspective. 

### 

### Criteria for system comparison

#### Polyglot persistence definition

The polyglot persistence problem is based on the premise that there is no single system which is effective when considering all types of data access, therefore multiple systems should be used in coordination to make all types of data access requirements of a given application feasible and performant. We call an application whose requirements cannot be met by any single storage system a polyglot persistence application.

#### The Problem

The problem of data integration has existed since the 1990's, but earlier manifestations were interested in aggregating information from disparate, evolving sources, and were not concerned with the issues that came with the Big Data era.


#### The Database Middleware

 - Forward approach
 - DBMS approach
 - Mediator approach


#### System comparison

Our goal is to express the polyglot persistence problem in terms of research that has already been done in the area of database integration.

#### Proposition 1

We want to compare different data integration systems which have been designed over the years in terms of criteria tailored around the challenges of a polyglot persistence application.

 - Data access pattern
 - Location/Availability/Ownership of data
 - flexibility of the number of data sources
 - Data velocity

#### Proposition 2

We want to select a number of criteria to classify the polyglot persistence problem in the space of data integration problems.

==> What is the space of data integration problems?
Not too sure yet.

One example : Information Manifold vs Cyclops.

"Bad" Goal :

 - Express the polyglot persistence problem in terms of research that has already been done in the area of database integration.

### Assumptions of Polyglot persistence

Multi-system application has a database middleware which "manages" underlying "one size" systems.

### Martin Fowler Challenges
 




### Challenges of Polyglot Persistence

Assemble the challenges with polyglot persistence identified by others in order to come up with a list of challenges.

Identified by others :

 - Shivnath Babu : DBMS+ system
   - How to integrate systems into the database middleware
   - Which systems to include in the database middleware
   - Which (distributed) execution plan to pick
   - How to provision resources : adapt to unusual workload?
   - How is the data stored : coupling storage and compute systems?
   - Describe what application requirements are

 - Martin Fowler : Polyglot Persistence Application
   - Learn interface for each data store.
   - Understand a lot about how the technology works to get decent speed.
   - NoSQL option involve running on large clusters which introduce a whole range of new questions about consistency and availability
   
 - Microsoft : Polyglot Persistence
   - The business logic of an application should not be dependent on the physical structure of the data that it processes ==> Use a unifying languages

##### My Challenges

 - Having a unifying query language for systems with varying query capabilities.
 - Enforcing integrity constraints.
 - Enforcing atomic transactions across multiple systems or any of the ACID guarantees across multiple systems.

### Existing Industry Solution : The Repository Pattern

The Repository Pattern is a software design pattern which centralizes all persistence concerns in a Repository Module.


#### Diversity of "One Size" Systems

Remember the figure from Babu's paper for a taxonomy of systems to be considered for PP.
