 - Email to : Yannis, Kian Win
 - Subject : Stateful vs stateless SQL++ wrappers

Hello all,

I am asking this question in the context of any SQL++ wrapper, not just AQL. I am asking this question as a general rule, out of any database-specific context :

	Is it desirable to have SQL++ wrappers be aware of the internal state of the native database they serve?

I include in state any of the following :

 - catalog information
 - partition information (if the underlying database is distributed).
 - any other information that is specific to that database instance.