## Problem setting

### RDBMS are getting beaten performance-wise by specialized systems in all areas including warehousing ...

##### Column store example

### But warehousing specialized systems are themselves dealing with new data

##### Explain how streams, graphs and semi-structured data cannot fit in column stores or traditional warehouses and performance numbers

##### Also motivate why multi-store can't be avoided (performance-wise)

## Multi-store architecture

### Industry Standard : the polyglot web service approach

### Garlic

### Aqualogic (?)

### Max Stream and Trill

### ESTOCADA

### DBMS+

### Miso Soup

For all of those we need performance metrics (or other metrics if performance isn't available) to compare warehousing workload (TPCH?) and show the benefit and challenges those architectures bring in. Show how each architecture is an improvement over individual specialized systems. 

## Forward and the work at UCSD

### SQL++ and Configurations

### Fededareted Middleware with SQL++ views


## Abstract

#### Notes

 - Big data analytics not operations.
 - We focus on multi-data-model architectures rather than multi-store architecure; we define the problem by what we are trying to solve, not the solution. 
 - We start by describing how RDMBS are not the one size fits all solution any more, refering to Stonebraker papers.
 - 2005 : We show column stores do much better than RDBMS in the data warehousing and analytics area. We also mention that similar situations occur in other areas such as OLTP, but we won't cover those in this talk.
 - 2010 : analytics have expanded from their typical TPC-H setting. People want to analyze new types of data such as weblogs (semi-structured, schemaless), social networks (graphs), monitoring and sensor data (streams).
 - Column stores were good for tpc-h, we are not suitable for those new data types. We investigate ongoing research in new database system architectures which allow this type of multi-model analytics.

#### Earlier Abstract

For a long time, SQL used to be the ”one size fits all” solution, in the sense that any application could meet all of its requirements using only a SQL database. In the Big Data era, a number of new specialized system have emerged to meet the needs of the ever increasingly complex applications. Turing Award winner Michael Stonebreaker announced in 2006 that ”the era of SQL had ended”, in the sense that for any given application requirement there exists a number of new specialized system that can beat SQL to it; but there are applications whose requirements cannot be met by any single database. This led to the emergence of the so called ”Polyglot Persistence” (PP) systems in which multiple specialized systems have to be used in coordination in order to meet all the requirements. Enabling such a coordination creates a number of challenges since specialized systems have been built to run independently and now have to be integrated together despite differing on a number of logical and architectural dimensions. In this paper, we present and discuss those challenges and analyze the current state of the art.














