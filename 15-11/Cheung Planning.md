## Cheung Planning

Outline : 

 - Show initial problem : web applications are running slow because of poorly designed code
   - Show example of analytics application
   - Show web application architecture
   - Show the java program currently used for execution and it's problems
 - Forward all declarative solution
   - Allows the data to be in session/database
   - Query processor makes best decision at the application level
 - Make some evaluations : show performance metrics between the use of the first solution and the second solution
 - Show what we would want to achieve at the java level.
 - Show Alvin Cheung's technique
   - Show sub example with fixed nation
   - Show inferred post-condition 
   - Show resulting code
   - Show process workflow slide from research exam (maybe add some information about templates, ask feedback from Ben if he thinks more info is needed)
 - Show what we have so far :
   - If we consider the sub fragment we can get the `sum` variable using Alvin Cheung's technique (only need to account for the extra variable)
   - We then talk about introducing the new axiom which uses the result of the subfragment to form a bigger statement.
   - Once both fragments are identified (and source-annotated) we can combine them into the final query.
 - Assuming what we have works :
   - Impact on Cheung's algorithm should be small, because templates don't increase in size and search space is only increased with the necessary variables.
   - Unknowns are how we identify the code fragments (we lack expertise on that domain, and which variables to add to the synthesis scope). It is very important we add the smallest number of variables possible, otherwise algorithm will blow up.
 - Nesting :
   - Show application in complex case
   - Show code for application
   - Show post-condition inferred from previous technique
   - Show how we can convert to SQL++ instead of SQL to make things work.