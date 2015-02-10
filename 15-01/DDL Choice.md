From what I can understand from last night's discussion, we have not made yet a  choice on :

 - what kind of DDL statements to expose in the context of the SQL++ interface. 
 - what kind of parser to use to handle SQL++.
 
 If this can be of any help, let me voice my opinion on the question.

Recall the choices we have on DDLs :

 a. We can opt to use a SQL++ syntax for all statements (DDL and DML).
 - We can opt to use SQL++ for queries only and use AQL for all other statement types.
 
Recall the choices we have on parsers : 

 1. Recall the characteristics of the SQL++ RI parser: 
    - It uses the ANTLR parsing technology while the AQL parser (and the currently existing SQL++ parser I built) uses JavaCC.
    - It does not include any DDL statements (SQL++ or otherwise).
 2. Recall the characteristics of the parser I built for SQL++ last quarter :
    - It uses the same technology as the existing AQL parser.
    - It does not support any DDL statements.
     
Effort required for each option :

 - **Choice a) (with parser 1 or 2)** : will require significant effort to figure out how to incorporate SQL++-style DDL statements in the existing Asterix infrastructure.
 - **Choice b) (with parser 1)** : will require replacing the existing parser with the SQL++ RI parser and reimplementing all AQL DDL statements using the ANTLR parsing technology.
 - **Choice b) (with parser 2)** : will require copying over DLL statements from the existing AQL parser to the SQL++ parser. It is the cheapest (effort-wise) option. 

My opinion :

 - Regarding the choice between a) and b) : I think it depends how important it is for us to have SQL++-style DDL statements.
 - Regarding the choice of parser : it lies in a trade-off between the short term extra cost of changing parsers vs the long term benefits of using the SQL++ RI parser (if any). I do not know what are the benefits of the SQL++ RI parser (Yannis and Kian Win are better suited to answer that question).
 
I am fine with any option, I just need to know which one we should be going for ASAP in order to make progress.
 
 Jules