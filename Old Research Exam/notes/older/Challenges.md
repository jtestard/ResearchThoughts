## Introduction

For a long time, SQL used to be the "one size fits all" solution, in the sense that any application could meet all of its requirements using only a SQL database.

In the Big Data era, a number of new specialized system have emerged to meet the needs of the ever increasingly complex applications.

Nowadays, however, for any given requirement there is a specialized ("one-size") system out there that beats SQL databases; but there are applications whose requirements cannot be met by any single database.

Applications requirements may also change over time, and the best system for the new requirements might not be the one in use beforehand.

This led to the emergence of so called "Polyglot Persistence" (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements.

## Challenges

Enabling such a coordination creates a number of challenges :

 1. How to choose which systems to integrate given a set of requirements?
 2. How do we integrate multiple specialized systems into the PP system?
   - Not all specialized systems have the same data model and query capabilities. How do we handle these differences? [semi structured data is the common data model]
 - How do we optimize queries in a PP system?
 - How do we provision resources for each specialized system (especially relevant since many specialized systems are meant to be run on clusters)?
 - How do we store data in the PP system?
 - How do we update specialized systems while preserving integrity in the presence of constraints and redundancy?
 - How can a PP system stay available?
 - How can a PP system deal with changes in the requirements of an application?

## Solutions

 - Forward
 - SOS
 - Cyclops
 - Martin Fowler & AdventureWorks (representative of adhoc PP systems created by the industry).
 - SmartCIS
 - APBM
 - Garlic?


## Solution Matrix

In the next section, we go over each challenge and present a grid of how the surveyed systems deal (or not) with that challenge.

### 1. How do we integrate multiple specialized systems into the PP system?
x
##### Note

You should explain in this section how queries are decomposed and sent to data sources, processed then returned to the virtual mediator. This is common across (basically) all surveyed solutions. Describe here only the process which allows this query to happen. Discuss optimizations later.

### 2. Not all specialized systems have the same data model and query capabilities. How do we handle these differences?

 - Forward : use semi structured data model (SQL++).
 - SOS : use semi structured data model (key-value with collection).
 - Cyclops : stream query model
 - APBM : relational data model
 - SmartCis : stream?
 - MaxStream : stream?
 - Martin Fowler & AdventureWorks : repository pattern, restful APIs

##### Note

Note how the query model depends on the context in which those applications are meant to run. No system attempts a completely global perspective. 

### 3. How do we optimize queries in a PP system

### 4.  How do we provision resources for each specialized system (especially relevant since many specialized systems are meant to be run on clusters)

### 5. How do we store data in the PP system

### 6. How do we update specialized systems while preserving integrity in the presence of constraints and redundancy

### 7.  How can a PP system stay available

### 8. How can a PP system deal with changes in the requirements of an application