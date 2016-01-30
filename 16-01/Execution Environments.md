# Execution Environments

#### Tasks for 2016/01/21

 - Read MapReduce/DBMS performance paper
 - Formalize execution environments to be considered in the rewriting context
 - Write this formalization in the paper and edit the scenarios accordingly

 
## Approaches to Large Scale Data Analysis paper summary

Two Approaches are being compared:

 - Map Reduce
 - Parrallel Data Warehouse (Vertica)
   - Row Store
   - Column Store

Providees very precise comparison of the charatecteristics of both systems in a number of areas (execution strategy, programming model...).

Presents a benchmark for execution which contains a series of tasks

 - Task 1 : Original MR Task (Grep)
 - Task 2 : Selection
 - Task 3 : Aggregation
 - Task 4 : Join
 - Task 5 : UDF aggregation

For each task, the data loading and task execution are specified for each execution environment.

---

#### Task 1 : Original MR Task (Grep)

##### PDW program:

```
SELECT * FROM data WHERE field LIKE `%XYZ%`
```

Execution Plan :

 - Full table scan

##### MR Program:

Map program only, filters out (K,V) pairs which don't match `%XYZ%`.

---

#### Task 2 : Selection

##### PDW program:

 ```
 SEKECT * FROM Rankings WHERE PageRank > x;
 ```
 
 Execution Plan:
 
  - Index Scan (per node)

##### MR Program:

Single Map function that splits input value based on field delimiter. No Index

---

### Task 3 : Aggregation

##### PDW Program

```
SELECT sourceIP, SUM(adRevenue)
FROM UserVisits
GROUP BY sourceIP;
```

Execution Plan:

 - Scan local table, extract sourceIP and AdRevenue (per node)
 - Local Group By (per node)
 - Global Group By (global)

##### MR Program

**Map** : split input value by field delimiter (given input record is a string) and produce {sourceIP:AdRevenue} key-value pair.

**Reduce** : Performs the aggregation by adding all adRevenus which have the same sourceIP.

---

### Task 4 : Join

---

### Task 5 : UDF aggregation

---

#### Notes

**Note**: While execution environments differ, number of nodes remains the same. 

**Note**: the task execution description shows the algorithm being run in each case, and some discussion to compare the two. This is identical to the task we need to complete in the rewriting context, albeit we would prefer formulas which could be specified within a cost-based optimizer. 

## Rewriting Execution Environments

The rewriting paper tackles the problem of :

 1. Discovering/signaling three equivalent expressions: (R0, R2 and R4)
 - Formalizing when the R2 expression is more efficient than R0 in a number of distinct execution environments.
   - Identify execution environments
   - Formalize a cost model for each execution environments
   - Formalize scenarios (scenarios are a (R0 subclass, Data Characteristics, Execution Environment) triple)
   - Find out the "theoretical" benefit through inequalities
 - Support efficiency claim with experiments

**Note**: We are always comparing distinct execution plans but in the same execution environment. 

Execution environment considered (max list, we might remove some if needed):

 - Middleware + Hive cluster (Hadoop ETL)
 - Middleware + PostgreSQL* (Visualization & WS)
 - AsterixDB (BDAS & WS)

*: by PostgreSQL, we mean a single machine database setup.

Database systems considered:

 - Postgres (RDBMS category)
 - AsterixDB (document store category)
 - Hive (Hadoop category)
 - Middleware 

**Note**: these systems are chosen a representatives of their category. We generalize our results to all systems to share the same described characteristiscs as those systems.


**Note**: We might want to revise outline from svn presentation to include  a separate section for execution environments considered.

Suppose full cost models are available (for every operator in each environment), then all we need to do is provide the following between the R0, R2 and R4 expressions for:

 - Scenario CGl using environment Hive ETL 
 - Scenario CGO using environment AsterixDB
 - Scenario CO using environment Forward
 - Scenario CGs using environment AsterixDB

**Question** : For each execution environment, should we compare/evaluate which rewriting (between R0, R2 and R4) is the most efficient for :

 1. Every possible scenario in which we can accurately determine which rewriting (between R0, R2 and R4) is the most efficient.
 2. One possible scenario in which we find that R2 or R4 is more efficient than R0.
 3. Every scenario from a chosen initial list of scenarios which matches a use case which utilizes the execution environment.

We should go with option 3. That being said, each use case description comes with one example which itself represents just 1 qualifying scenario out of the possible multiple ones that could qualify.

What we need by Wednesday:

 - The matching scenarios for every execution environment.
 - A full description of cost models for all three execution environments. (By monday morning) We can put it in one big table. 
 - All the equations. Assumptions should come in later. We also want the results of the experiments, because we want to know if we want to target cost-based or rule based optimizers.

Notice that by comparison, the guys in Pavlo don't provide very accurate (only discussed) cost models. But they don't describe an optimizer, they only compare execution environments. We have to put ourselves in the idea that what we are building is a cost model, therefore we want formulas a cost-based optimizer could  
use. Noting that if we can justify that some form is ALWAYS better, a rule-based approach can be used instead.

We now describe each execution environment:

### Approaches to writing section 5

**Option 1**:

 - Divide by reach/output
 - Reason about all QPs at the same time
 - Divide by environment (up to two envs for a given reach/output option)
 - Use data characteristics (e.g. # of distinct values) to determine which physical operators are used, thus cost model results and comparisons
 
**Option 2**:

 - Divide by QP
 - Divide by execution environment
 - Divide by reach/output
 - Divide by data characteristics (# distinct values)

|   table   	| Option 1 	| Option 2 	|
|------	|----------	|----------	|
| Pros 	|   w        	|    i      	|
| Cons 	|   w       	|     j     	|