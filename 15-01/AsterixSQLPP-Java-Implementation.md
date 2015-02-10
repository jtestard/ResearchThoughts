## Asterix SQLPP Java implementation Meeting

*The class hierarchy for the java implementation of the new language should provide a clear way to add implementation for any new language.*

Michael Carey :)


## Part 1 : Implementation


### Presentation
See slides for [implementation details](https://docs.google.com/a/eng.ucsd.edu/presentation/d/1RKeLq4xIKvLemEagvB-iqrgtlCnjA6wUvps0t4uMvRw/edit#slide=id.p11).

### Conclusions

#### Visitor Pattern

 - See if the current AST to plan translation process (which does a tree traversal using the visitor pattern) is "clean". By "clean", we mean that the resulting subplan obtained by visiting a subtree does not need to be rewritten.
 - Monitor the time required to write the visitor and understand the . If there is something which takes an abnormal amount of time.


#### Isolated Translation Module

Ideally, we would like the SQL++ AST to plan translation to be as rely as little as  possible on 

 - Is it possible to isolate completely the AST to plan translation process if no validation needs to be performed?
 - Besides validation, is there anything else which would prevent us from doing the AST to plan translation?
   - Hyracks job creation : can we refactor it?

#### Refactorings

 - We want to refactor the system such that the artifacts (fuzzy) necessary for the plan translation are separated from those that aren't.
 
#### Appearance of Interface

 - How do we want the SQL++ interface to appear to the user? 
 - Will it be possible to mix and match AQL and SQL++ statements?
   - Do we want SQL++ insert statements or should we be content with AQL for non-query statements?
 - The draft architecture allows to have a list of (query language wise) heterogeneous parsed statements but does not provide a parser which can deal with both SQL++ and AQL.

#### Multiple query languages

 - Do we want an easy way to add any new language "foo" or is it OK to just have an adhoc way of adding SQL++ support?
   - If multiple language support is only transient, i.e. we eventually have all of our query processing using SQL++, maybe it is not so important to have such a feature.
 - We should suggest a way to combine AQL and SQL++ within an interpreter. Have the SQL++ statement be prepended by an identifier to allow the use of a different parser for them (we don't wnat a combined AQL/SQL++ parser).

#### Notes to self

 - New terms are fuzzy. If you need to introduce a new term to explain a concept, prefer an example instead.


### Topics

 1. Actual Translation
 - Presentation
 - Plumbing

#### I. Actual Translation

#### Some observations 

##### 1. No need for Asterix metadata (or Hyracks instance)

The problem we are trying to solve is to take a SQL++ query and translate that query into a logical plan which Asterix can execute. 

To the best of my knowledge, in order to the actual translation of SQL++ queries, if we don't take into account the use of UDFs, then it is possible to solve the entire problem without accessing Asterix metadata (or even starting a Hyracks instance). My reason to believe this are the following :

Metadata isn't required to parse the SQL++ query into an AST. I have found three different reasons the Asterix metadata is used during to translate the AST into a logical plan:

   a. Initializing the variable counter for the translation context.
   - Looking up UDFs. 
   - Provide the ResultSetId information for the DistributeResultOperator.

a) This issue is not a problem because the metadata is not necessary to obtain this information. Indeed, the variable counter is initialized during the parsing process and just "carried over" inside the metadata data structure. We can just define a simple alternative data structure which carries over that information.

b) Given we currently don't take UDFs into account, this won't be an issue.

c) Each query result is associated with a ResultSetId, which is determined by the Hyracks instance. This ResultSetId is then necessary to create the top-level DistributeResultOperator which is added at the very end and is never used in the translation process. An example of a logical plan obtained with the query shown below : 

```
distribute result [%0->$$0] -- |UNPARTITIONED|
  project ([$$0]) -- |UNPARTITIONED|
    unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}] -- |UNPARTITIONED|
      empty-tuple-source -- |UNPARTITIONED|
```
A solution to solve this problem is to build a plan with the ProjectOperator as top-level element and add the DistributeResultOperator as soon as we have access to Asterix metadata again.

One final issue I had was that I wasn't able to pinpoint where the verification of existence of a dataset occurs by just looking at the code. I noticed that when using the online interface and I input the query seen above (but with an non-existing dataset name), the logical plan is printed before an error is thrown. As such, I assume that the dataset lookup occurs **after** the initial logical plan is fully generated, but I would like to confirm with you guys.

I have conceived the design of the SQL++ interface with this observation in mind. The design itself can be seen in the attached Google Presentation.

##### 2. SQLPP AST Rewriting

In the case of AQL, there are some AST rewriting patterns (such as let clause wrapping). In the case of SQL++, we will need to rewrite the query to make the use of variables more explicit (see example). For example, take the following two queries in SQL++ ...

a) SELECT fb.alias FROM FacebookUsers AS fb

b) SELECT alias FROM FacebookUsers
   
... and their equivalent in AQL :  

c) for $fb in dataset FacebookUsers return $fb.alias

We currently support the a) syntax, but not the b). The intention is to add support for the b) syntax using an AST rewriting. For the moment, no rewriting exists.


#### II. Presentation

I have a read your suggestion :

*For the "routing" of AQL vs SQL++ Mike suggests that SQL++ statements go to one service and AQL statements to another separate service.*  
 
But actually things are not so simple, because some AQL statements are (to the best of my knowledge) necessary for any AQL program to work, such as the dataverse specification statement : 

	use dataverse <DataverseName>;

I am not sure what to do if the SQL++ endpoint is not allowed to issue **any** AQL statement. We could say that only the `use dataverse` statement is allowed, but we might as well allow a mix and match. I suggest a design which can mix and match AQL and SQL++ statements. We can always further restrict what kind of statements we want to allow on a given endpoint if we wish to.

I suggest for this purpose a 4 step solution :

  a. Split input program into statements.
     - the `select` keyword doesn't exist in AQL. A way to distinguish SQL++ statements from AQL would be to look at the first keyword of each statement and consider it to be SQL++ if the first keyword is `select` (and AQL otherwise). Another method would be to have a token which identifies as statement as being SQL++. Please tell me which solution you would prefer.
  2. Identify the AQL and SQL++ statements and separate them. a) and b) can be done using a small "pre-parser".
  3. Parse statements individually and then assemble the statements back as a single list, preserving the initial order.
  4. Submit the list of mixed and matched statements to the translation module for processing. 	

#### III. Plumbing and refactoring

The refactorings I would wish to introduce are limited to the APIFramework class, which is responsible for taking transforming an AQL AST into a Hyracks Job specification. It currently contains two methods :

   a. ```public static Pair<Query, Integer> reWriteQuery(...)```
   - ```public static JobSpecification compileQuery(...)```
   
And :
   
 - a) is responsible for doing rewritings of the AST (such as let-clause wrapping). It also prints the AST before the rewriting occurs.
 - b) takes a rewritten AST and transforms it into a Hyracks Job specification. It has a lot of not-so-related responsibilities that can be broken down into smaller, reusable methods.

My suggestion is to break down a) and b) into the following smaller methods :

 - Break ```Pair<Query, Integer> reWriteQuery(...)``` into :
    - `printAST(...)`
    - `rewriteAST(...)`
    - `printRewrittenAST(...)`
 - Break ```public static JobSpecification compileQuery(...)``` into :
    - `translateASTtoLogicalPlan()`
    - `printLogicalPlan()`
    - `optimizePlan()`
    - `printOptimizedPlan()`
    - `generateJobSpec()`
    - `printJobSepc()`

### Observations

 - The AST rewriting process is AQL specific and does not contain any rewriting that would be inherently required in the context of SQL++.
 - The validateOperation found in the AbstractAQLTranslator class does not affect queries.
 - In the actual ASTtoPlan Translation process, the metadata provider is only used for 
   - initializing the variable counter for the context. => not a problem (we can generate ourselves)
   - looking up UDFs. 
   - Provide the ResultSetId information for the DistributeResultOperator. => Can obtain before translation process begins? Or add the DistributeResultOperator after the plan translation.
 - As expected by Yannis, up to now no reordering of operators occurs in the initial translation process.
 - We need to create Ids for the variables when parsing in SQL++.
 - The translation context keeps track of variables in AQL and we'll need to do the same thing in SQL++.
 - Builtin-functions lookup does not require metadata lookup (kin).
 - In the context of handling an AQL query, the OutputDataset is set always null.
 - No SQL++ AST rewriting patterns have yet been identified. 

Problem : cannot find verification of existance of dataset. Given that the interface is capable of determining the nature of the logical plan without throwing an error, (when specifying an invalid dataset, the error is thrown when attempting to produce an optimized plan) we will assume that (to be verified with the Asterix guys).

 - Does function call correctness validation happen before or after the generation of the initial logical plan? It would seem that in the case of dataset name validation, this happens after.
 
 - The ResultSetId uniquely identifies the result of a query. It is only used within the LogicalPlan for the distributeOperator, which itself is never really used in the plan. We can create a logical plan in an isolated module (without starting a hyracks instance) except for that operator.

### TODOs

 - Change dataset to function call in SQLPP AST.
 - Add id naming to SQLPP AST.
 - A suggested implementation would be to have, instead of the AQL...
   - ```[1] public static Pair<Query, Integer> reWriteQuery(List<FunctionDecl> declaredFunctions, AqlMetadataProvider metadataProvider, Query q, SessionConfig pc, PrintWriter out, OutputFormat pdf)```
   - ```[2] public static JobSpecification compileQuery(List<FunctionDecl> declaredFunctions, AqlMetadataProvider queryMetadataProvider, Query rwQ, int varCounter, String outputDatasetName, SessionConfig pc, PrintWriter out, OutputFormat pdf, ICompiledDmlStatement statement)```
 - Would be to have :
   - ```[3] public static ILogicalPlan translateQueryToLogicalPlan(SQLPPQuery query, List<FunctionDecl> declaredFunctions, AqlMetadataProvider metadataProvider, int currentVarCounter, String outputDatasetName)```
   - ```[4] public static JobSpecification compilePlan(List<FunctionDecl> declaredFunctions, AqlMetadataProvider queryMetadataProvider, ILogicalPLan, int varCounter, String outputDatasetName, SessionConfig pc, PrintWriter out, OutputFormat pdf)```
 - The translateQueryToLogicalPlan is where the fun stuff happens. 
 - The compilePlan just repeats what exists in the code once the initial logical plan is obtained. 
 - Note the `ICompiledDmlStatement statement` argument is not necessary because we are only dealing with queries here.
 - Additional suggested refactoring (non essential) :
  - break down methods in the `rewriteCompileQuery()` instead into :
    - `printAST()`
    - `rewriteAST()`
    - `printRewrittenAST()`
    - `translateASTtoLogicalPlan()`
    - `printLogicalPlan()`
    - `optimizePlan()`
    - `printOptimizedPlan()`
    - `generateJobSpec()`
    - `printJobSepc()`

The problem we are faced at this point is whether the `AqlMetadataProvider metadataProvider`, `List<FunctionDecl> declaredFunctions` and `int currentVarCounter` are necessary to the creation of the logical plan. 

### Notes
 - Query may or may not be a part of a transaction (shouldn't matter for us).
 - What is the difference between the `PlanPlotter` and the `PlanPrettyPrinter`?
 - What is the `int varCounter` used for? 
 
### Questions to Mike

Hello Mike and Yingyi,

I have come up with an initial draft of the design of the SQL++ interface. The design itself is shown in the form of a Google presentation available here : https://docs.google.com/a/eng.ucsd.edu/presentation/d/1RKeLq4xIKvLemEagvB-iqrgtlCnjA6wUvps0t4uMvRw/edit.

I would like to skype with you, Yingyi, to make sure we agree on the design before I go any further.

Before discussing the design, I wish to submit to you a series of questions. 