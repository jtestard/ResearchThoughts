### Chunbin's Presentation Notes

Note :

Provide initial background : such as transactions and cloud.

Describe transactions in two slides : 

1) Transactions in general

 - atomicity : a transaction may contain multiple operations. All of them should happen or all of them shouldn't happen (no inbetween).
 - consistency : the successful or failed execution of a transaction should leave the database in a consistent state.
 - isolation : mulitple transactions should be correctly processed simultaneously.
 - durability : in case of sudden crash of the system, the system should recover in a way which satisfies consistency. 


2) Transactions in the cloud

 - availability : services should be available l
 - scalability : services should be able to handle variations in request load.
 - responsiveness : services should respond to user requests with minimum delay.
 

### The CAP theorem


### Eventual consistency

Fundamental approaches :

 - CloudTPS
 - ElasTras
 - G store

Response approaches

 - deuteronomy
 - heterogeneous KV stores