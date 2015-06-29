## Cuts

### The multi-store motivation

##### Heterogeneity of data models

 - Forward
 - MaxStream
 - Invisible Glue
 - Cloudy
 - SOS
 - ODBAPI
 - Microsoft Adventure Works

##### Heterogeneity of query workloads given a fixed data model

 - DBMS+
 - Miso Soup
 - Max Stream
 - Cloudy

### The data integration vs co-design divide

##### Data Integration
 - Trying to leverage existing (maybe already in use) specialized systems and coordinate them to handle more complex application requirements. 
   - Max Stream
   - Forward
   - Estocada
   - SOS
   - Microsoft Adventure Works
   - Martin Fowler

##### Co-design
 - Build a totally new application in which specialized systems are combined to yield higher performance.
   - DBMS+
   - Miso Soup

 
Problem : currently state of the art systems are tuned to specific data models and query workloads, but the number of targets is ever increasing and the number of systems used to handle them as well. 
 
2 examples which motivate the problem :
 
  - Warehousing with heterogenous data models
  - Streaming applications with heterogeneous query workloads
 
More often than not, those change in requirements come when an application has already been built with existing system. In order to solve problems for which no specialized systems has yet been designed, instead of creating yet another specialized systems we propose to coordinate existing storage systems into achieving the problem by leveraging their capabilities.
 
 A state of the art architecture which solves the problem but with some overheads : M
 
 The flaws of such an architecture :
 
 The research solutions :