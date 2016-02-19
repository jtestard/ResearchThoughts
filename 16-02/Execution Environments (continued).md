## Execution Environments (continued)

We consider the possibility of unifying all considered architectures into a single one.

Our architecture has two main components:

 - **Middleware**: capable of writing to disk, with a memory capacity M_M and a capability to push down computation to capable data source. I see a problem here when we reach experiments. I only know two kinds of middlewares (FORWARD middleware and Informatica), none of which has exactly such capabilities.
   - The middleware is capable of running any operator from the SQL++ algebra.
 - **Data sources**: we consider three kinds of data sources, a file system, a traditional RDBMS and a semi-structured database. We will be choosing PostgreSQL and AsterixDB as representative of those two categories.
   - **File System**: this source has no capabilities, and the middleware cannot push down any operator to it.
   - **RDBMS**: this source is relational-capable, and the middleware can push down any purely relational operator to it. Need to define purely relational operator
   - **AsterixDB**: this source is SQL++-capable, and can process any operation from the SQL++ algebra.