Hello Yannis,

I have done the decision-making exercise you suggested and have come to the following conclusion.

### What I can't do

 - Focusing solely on decorrelation involving a relational database system is not a good option, because there isn't that much new work being done in that area. Moreover, this line of work does not correspond well to my ideas for future research.
 - Focusing solely on application program rewriting is not a good option either, because I don't have the necessary background in program analysis and SMT solvers (Alvin Cheung's work).

### What I can do

What I can do is focus on the problem of tuple-at-a-time (LAAT) vs set-at-a-time execution (SAAT) in the web application context. This is a very relevant real-world context, many developers face performance issues because they write code by looping over parameterized queries. The problem can be formulated as :

*How can web applications answer analytical queries more efficiently than using the tuple-at-a-time technique?*

Query decorrelation shows how the database world has been dealing with this issue and constitutes a background for this line of work. Static analysis and automatic program rewriting constitutes one solution, but other solutions exist (such as FORWARD).

### Revised Outline

- Introduction
   - Web application performance : a real world problem
   - Web application architecture
   - Tuple-at-a-time code example
   - The problem
   - Outline
- Background : query decorrelation
  - Tuple at a time execution
  - Set at a time execution
  - Magic Decorrelation
- FORWARD & SQL++
   - Analytics Application Example
   - Single Semi-Structured Query
   - Forward Architecture
   - Algebraic Rewriting
   - Pros & Cons
- Rewriting procedures with batched bindings
   - Approach
   - Example
   - Query Batching Step 1 : Loop Fission
   - Query Batching Step 2 : Set Oriented Execution
   - Performance benefit
   - Pros & cons
- Query Synthesis
   - Relational Join in imperative code
   - Query Synthesis
   - Translation Process
   - Performance benefit
   - Pros & Cons
- Comparison 
  - Comparison (sums up pros & cons)
- Future Work
  - Query Synthesis with SQL++


-------

### Intro

 - Web applications represent are a huge industry which has been growing for long time & continues to grow.
 - Web applications require prompt response times ( < 1 sec) when returning to the user, making good performance a necessity. 
 - Web applications store their data in a database, and need to compute analytics queries over that database quickly and efficiently.
 - That is a hard task, which requires knowledge that not every user possesses . 

### Background
The problem of query decorrelation has been studied for a long time in the realm of database systems. 

My work consist of doing a survey of the different techniques used to solve this issue :

 - FORWARD : rewrite the application in SQL++. The FORWARD query compiler can then choose the best query plan (which will perform set-at-a-time execution)
 - Sudarshan : identify code fragments that can be rewritten into set-at-a-time plans and then rewrite them using rewriting rules/
 - Alvin Cheung : identify code fragments, use VCs and a SMT solver to generate a relational expression for the code fragment and rewrite the program accordingly.

My solution is to break the exam into two parts : 

 - The first part focuses on query decorrelation and the problem of tuple-at-a-time vs set-at-a-time execution, in a database/middleware only context.
 - The second part extends the tuple-at-a time vs set-at-a-time discussion to database applications written in imperative language, and how efficient program transformations can be achieved using static analysis.



