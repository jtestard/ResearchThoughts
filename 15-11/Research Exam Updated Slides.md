### Research Exam Updated Slides

 - Put LINQ work at the end.
 - **Don't** put it on the outline.
 - Consider it part of "other techniques", don't highlight it.
 - Don't put code examples (the one in the report is probably big).
 - Put LINQ and switch in the middle of "other approaches" to integrate data into programming languages (embedded querying). Talk about some of the problems "these techniques" face. 

 
 
 - Other Approaches: 
   - LINQ
   - Switch (Ruby DSL)
   - e
 

You want to say: we add it for completeness but we don't focus on it.

3 choices :

 - Go full length on LINQ (5-6 slides, 10 minutes) : becomes major component of the talk (on par with batching and synthesis). 
   - Slide
     1. LINQ as an alternative to integrate nested data, includes LINQ architecture 
     2. Show how linq deals with the query for example 2, and derive the fact that a query avalanche occurs, as well as the operator chain.
     3. Each SQO is a list comprehension, with a syntax of the form [x1,...,xn].select(x => ) *equiv* to a map() operation
     4. Chains of map can be changed to relational algebra using loop-lifting, based on the transforming the iteration into an operator which inputs table with an `iter` and `pos` column, and outputs a table (==> relational algebra).
     5. The different composent are transformed into a query plan through a compilation process. Multiple queries may be issued, therefore the plan may have multiple roots. 
   - Good
     - Completness is full
     - No risk of having weak section
   - Bad
     - Time consuming
     - Might make overtime
     - Will have less time to fully absorb material, have a risk of creating attack openings for committee
     - Will contrast with the short aspect of the report
 - Go smaller section with Beyond SQL (2-3 slides, 5 mintues) : becomes interesting extension
   - Slide
     1. LINQ as an alternative to integrate nested data, includes LINQ architecture 
     2. Show how linq deals with the query for example 2, and derive the fact that a query avalanche occurs. 
   - Good
     - Timing stays right
     - Doable without too much trouble
   - Bad
     - May look like essential component that was left off if not done properly.
 - Go single slide with Beyond SQL (1 slide, 2 minutes) : related work that people may be interested in.
  - Slide
      1. Approaches other than FORWARD for integrate persistent data into application programming language. 1) explain LINQ, 2) explain nested data model, 3) explain tuple at a time 
  - Good
     - Very easy to make
     - Bad

