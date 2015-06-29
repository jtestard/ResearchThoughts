ORM : we show how Alvin Cheung, Sudarshan, Gurst and Forward aim to make our lives easier by allowing the comfort of ORMs and the efficiency of handcrafted SQL.

 - Impedance mismatch problem.
 - Poor performance in database applications comes from programs accessing the database in inefficient ways, ORMs are a good example.
 - Database query optimization can't solve the problem because the database is unaware of the application program.
 - Programs can be manually rewritten to obtain better performance, but the process is error-prone.

**Research Problem** : How can we get database applications to perform without manually rewriting the application program?

 - **Sudarshan Lab**
   - Use static analysis to transform ORM programs to use batch queries instead.
   - Static analysis can also be use to make asynchronous querying and asynchronouse batches.
   - Static analysis used for prefetching queries
 - **Alvin Cheung**
   - Use program synthesis to generate more efficient queries from ORM-fueled procedural programs.
 - **Forward**
   - Replace ORMs by a declarative language (SQL++) within the Forward platform. Only works within a web application context.


### Alvin Cheung QBS

See later : 

 - Theorem 1 proof
 - Section 2.1
 - Section 4.1



Program Synthesis Process :

 1. Locate all persistent data methods
 2. For each persistent data method, inline a neighbourhood of calls which will give a you a code fragment
 3. For each code fragment, detect the result variable
 4. Translate each code gragment into kernel language
 5. Compute verification conditions (VC) for the code fragment
 6. Compute invariants and post conditions from the VCs. Post-condition is expressed in a predicate language based on the theory of ordered relations (relational algebra on arrays instead of bags)
 7. Prove invariants and post-condition using a theorem prover
 8. Translate predicate language expressions into translatable expressions using a set of rules (which is complete)
 9. Translatable expressions can be converted to SQL


PL Concepts :

 - Hoare Logic
 - Verification Condition
 - Pre/post condition and invariants
 - Automatic Theorem Proving