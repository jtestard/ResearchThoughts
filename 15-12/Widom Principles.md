## Widom Principles

In this document, we discuss violations of the widom principles in the data access paper. In addition we may express some opinion about what could be done for improvement.

#### Running Example

#### Paper Title

#### The Abstract

Widom suggests the following requirements for the abstract:

 - State the problem and motivation
 - State your approach and solution
 - State the main contributions of the paper

##### Problems

1. The motivation currently targets onlys inefficiencies caused by ORMs. If we want to target NoSQL databases, we need to add that to our motivation.
2. I don't understand the following sentence *full generality*


---
### Notes

Quote : *These objects can be defined in different programming languages and type systems, in constrast to conventional integration systems.*

Minor point: a number of web frameworks no longer use relational databases as their backend. Indeed, meteor (ranked as #7 most used by http://hotframeworks.com/) is a web framework which is mongo-only compatible.


```
db.nations.where(...).customers.
```



### Suggestions 

 - Find example with greater fanout than selected nations

---

Section 4.1 discusses the semi-structured algebra.