## AsterixDB SQL++ Wrapper Interface Comparsion

#### Objective

The objective is to write a SQL++ wrapper for AsterixDB for the forward SQL++ processor. 
Three interface options are available to build that wrapper :

#### Options

 - Interact with the AsterixDB user layer. The language used by the user layer is called AQL. The AsterixDB query processor will translate AQL queries into an Algebricks DAG.
 - Interact with Algebricks, the algebra layer of Asterix. Algebricks takes as input an Algebricks DAG, which is a direct acyclic graph of relational algebra operators. It then optimizes it according to rewriting rules and outputs a Hyracks job specification.
 - Interact with the data-computing platform on which AQL is based, called Hyracks. Hyracks tasks are specified using Hyracks job specifications directly.

#### Evaluation Criteria

We wish to evaluate which of the three options is the most beneficial for the SQL++ wrapper implementation given the following criteria :

 - Simplicity : one option is simpler (less complex, less time consuming...) than the other.

 - Soundness : implementing the option does not require violating some design assumptions for the SQL++ wrapper.
 
#### Design assumption : stateless

We have only one design assumption :

 - The SQL++ wrapper should not be aware of the internal state of the native database system it is communicating with.

#### Design assumption : stateful


### Questions

**Question 1 :** Do AQL queries get translated into Hyracks job specification or something different (such as a Hyracks Activity Node graph)?

**Answer :** The short answer is yes. AQL queries are translated into a query plan representation called an Algebricks DAG, which itself then optimized and translated into a Hyracks Job Specification.

**Question 2:** What does it mean for a Hyracks job specification to be better than another?

**Answer :** A Hyracks job specification can be likened to a directed acylic graph where :

  - nodes are physical operators
  - edges define the direction of the data processing flow.


### Resources

  - Look at [hyracks paper](http://www.ics.uci.edu/~rares/pub/icde11-borkar.pdf), in particular the section on its interface.
  - AQL's interface can be found [here](https://asterixdb.ics.uci.edu/documentation/aql/manual.html).

### Ideas

 - AQL is a SQL-like query language : maybe easier?
 - Hyrack's input are plans. Forward's output are plans. maybe easier?
 
### Draft

Hyracks is distributed, and the specification of scanner operators requires knowledge of where partitions of data collections are located.

If the Hyracks option is chosen, the stateless assumption of the SQL++ wrappers would be broken.

My opinion is that the SQL++ wrapper should not be aware of the internal state of the native database system.

Efficiency here is meant purely qualitatively. It is only based on the structure of the Hyracks Job Specification (or physical distributed query plan) and not on any performance metrics.

I am not 100% sure on the design assumption. It is sensible to have the wrapper be aware of information such as the catalog.

### Notes to self 

Criteria for selecting best options are very vague.

### Efficiency
 - Efficiency : one option is *better* than the other.
We now define what mean by an option being *more efficient* than another.

Given an SQL++ query, the Forward query processor will generate a distributed, source annotated plan *P*. 

Consider a subplan *S* of *P* such that all operators in S have been assigned to AsterixDB. We say that option A is *more efficient* than option B if :

 - For all such *S*, the ultimate translation into a Hyracks job specification generated using option A is  at least as efficient as the one generated using option B.
 - There exists an *S* such that the ultimate translation into a Hyracks job specification generated using option A is *more efficient* than that generated using option B.

#### Definition of efficiency

A Hyracks job specification is a dataflow graph where :

 - Nodes are physical operators (HashJoin, HashGroupBy ...).
 - Edges define the direction of the data processing flow. Edges are annotated with data distribution logic from the source to the target partitions.
