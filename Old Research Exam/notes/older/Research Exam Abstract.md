## Abstract 1

For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database. In the Big Data era, a number of new specialized system have emerged to meet the needs of the ever increasingly complex applications. Turing Award winner Michael Stonebreaker announced in 2006 that "the era of SQL had ended", in the sense that for any given application requirement there exists a number of new specialized system that can beat SQL to it; but there are applications whose requirements cannot be met by any single database. This led to the emergence of the so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite differing on a number of logical and architectural dimensions.

In this paper, we propose a middleware architecture for PP systems in which multiple specialized systems run on the same cluster, with a common entrypoint for querying and updating using a unifying semi structured query language and data model. The PP system's query optimizer chooses on which specialized system(s) the query will execute using a variety of surveyed federated database query optimization techniques. Next, we see how the PP system can be updated while preserving integrity in the presence of constraints and redundancy. Finally, we survey how the PP system can be made to declaratively specify features such as staleness, availability and flexibility to change in application requirements. 

------ 

Instead of second paragraph :

In this paper, we survey existing architectures for PP systems. First, we look at how the surveyed systems integrate multiple specialized systems into a PP system and handle the data model and query capabilities heterogeneity among the specialized systems. Second, we look at how the surveyed PP systems distribute the query execution among the specialized systems. Third, we look at how surveyed PP systems handle storage in the specialized systems and, when relevant, provision resources for them. Fifth, how the PP system can be updated while preserving integrity in the presence of constraints and redundancy among specialized systems. Finally, we survey how PP systems can be made to allow declarative specification of features such as staleness, availability and flexibility to change in application requirements.






## Abstract 2

In the Big Data era, the specialized system dominate, but some application's needs still aren't met by any given specialized system. This led to the emergence of so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite having different data models and query capabilities.

## Thought process

<!--
Michael Stonebreaker announced in a 2006 paper that "the era of SQL has ended", in the sense that for any given application requirement there exists a number of new specialized system that can beat SQL to it.
-->

For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database.

In the Big Data era, a number of new specialized system have emerged to meet the needs of the ever increasingly complex applications.

Nowadays, however, for any given requirement there is a specialized ("one-size") system out there that beats SQL databases; but there are applications whose requirements cannot be met by any single database.

Applications requirements may also change over time, and the best system for the new requirements might not be the one in use beforehand.

This led to the emergence of so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements.

Enabling such a coordination creates a number of challenges :

 1. How do we integrate multiple specialized systems into the PP system?
 - Not all specialized systems have the same data model and query capabilities. How do we handle these differences? [semi structured data is the common data model]
 - How do we optimize queries in a PP system?
 - How do we provision resources for each specialized system (especially relevant since many specialized systems are meant to be run on clusters)?
 - How do we store data in the PP system?
 - How do we update specialized systems while preserving integrity in the presence of constraints and redundancy?
 - How can a PP system stay available?
 - How can a PP system deal with changes in the requirements of an application?

Extra challenge : Which systems to include for a given set of requirements? [consider system choosing as an input to the problem]

In this paper, we propose an architecture which tackles all of those challenges by combining solutions devised after years of database research for each problem.

 1. The architecture is a mediator-style middleware architecture. 
 	- The PP system provides a single point of entry for querying and updating.
 - We show that the semi structured data model comes as the ideal candidate for the common data model and use XQuery/SQL++ for querying.
 - Distributed query optimization techniques depend on the storage system configuration [assumes the mediator has an execution engine (differs from Babu's paper)]:
   - If the storage system is tightly coupled with the specialized system's execution engine (typical operational case), then formulating a distributed query plans amounts to choosing which operator should be handled in middleware and which should be offloaded to the specialized system.
   - If the storage system is independant from the specialized system's execution engine (typical Hadoop case), then the question can become which specialized system should be used for query execution.
 - We survey techniques mentioned in Babu's paper.
 - Hadoop-based systems allow a decoupling of storage and execution while NoSQL databases and traditional RDBMS have the two tightly coupled.
 - updates
 - availability
 - changes

Many of those specialized systems are meant to be run on cluster of machines, and we describe how the PP system can make multiple systems run on the same cluster and provision them accordingly.


 
Coordination avoidance ==> multi-partition isolation.

As Martin Fowler puts it's "[creating ad-hoc PP system] increases complexity in programming and operations", in this paper we go over the challenges and solutions to the problem.

#### Suggested sections 


### Email

Hello everyone,

I am doing my research exam this quarter. I am about 40% of the way there, in the sense that I think I have a pretty good idea of the dimensions of my topic but haven't read all the papers yet. I present to you my abstract in which I present my vision and what I wish to cover. It's one of my first paper writing exercises, so I am looking forward to any type of feedback.


*For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database. In the Big Data era, a number of new specialized systems have emerged to meet the needs of the ever increasingly complex applications. Turing Award winner Michael Stonebreaker announced in 2006 that "the era of SQL has ended", in the sense that for any given application requirement there exists a number of new specialized systems that can beat RDBMSes to it; but there are applications whose requirements cannot be met by any single database. This led to the emergence of the so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite differing on a number of logical and architectural dimensions.*

*In this paper, we propose a middleware architecture for PP systems in which multiple specialized systems run on the same cluster, with a common entrypoint for querying and updating using a unifying semi structured query language and data model. The PP system's query optimizer chooses on which specialized system(s) the query will execute using a variety of surveyed federated database query optimization techniques. Next, we see how the PP system can be updated while preserving integrity in the presence of constraints and redundancy. Finally, we survey how the PP system can be made to declaratively specify features such as staleness, availability and flexibility to change in application requirements.* 

Thank you so much for your time,

-- Jules


### More attempts

In this paper, we survey existing architectures for PP systems. First, we look at how the surveyed systems integrate multiple specialized systems into a PP system. Second, we look at how the surveyed PP systems handle the data model and query capabilities heterogeneity among the specialized systems. Third, we look at how the surveyed PP systems choose on which specialized system(s) the query will execute. Fourth, we look at how surveyed PP systems store the specialized systems and, when relevant, provision resources for them. Fifth, how the PP system can be updated while preserving integrity in the presence of constraints and redundancy among specialized systems. Finally, we survey how PP systems can be made to allow declarative specification of features such as staleness, availability and flexibility to change in application requirements.




### ewe

Each PP system that we surveyed only tackles a subset of the challenges above, because they target only a subset of the more general PP problem. We propose an architecture about how those systems might be combined to form such a general solution.




-----

The PP system's query optimizer chooses on which specialized system(s) the query will execute using a variety of surveyed federated database query optimization techniques.



specialized systems have the same data model and query capabilities

middleware