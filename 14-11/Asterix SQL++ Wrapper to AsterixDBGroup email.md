### SQL++ Wrapper in AsterixDB
Recently, there have been talks of adding a new user interface to Asterix, in addition to the original AQL interface, based on the SQL++ language. But first, let me put some context.


### Context
At UCSD, we are working on a "new generation" query processor called Forward, meant to tackle the challenges imposed by the increased variety of data models found nowadays in both industry and academia.

Forward is the database middleware meant to support simulatenously mutliple data sources with varying data models (structured or semi-structured). We chose AsterixDB as the first semi-structured data source we wish Forward to support.

The interface to Forward itself is a language called SQL++, which is meant to be a superset of SQL and JSON, with its own data model (the SQL++ data model). It is a very permissive language, and both SQL and AQL can be modelled as subsets of SQL++. Details on SQL++ and its data model can be found [here](http://arxiv.org/abs/1405.3631v4). As such, the SQL++ interface will only support the *Asterix-compatible* SQL++ subset.

### Interface Implementation

While the documentation for the existing interfaces of Asterix is very good, I haven't been able to find much about the internal structure about the Asterix Data Management System (the AQL layer, if I understand correctly) and the Algebricks layer. Most of my knowledge come from reading the source code of the project. As such, a number of assumptions have been made about the internals which might be incorrect. Most of this understanding comes from reading the `compileQuery()` method of the `APIFramework` class:

 1. A `AqlExpressionToPlanTranslator` object is created from the current context.
 2. In the , a **logical plan** is built from the input AQL query using the translator object.
 3. From this plan (and other metadata), a **compiler** is built. The plan from which the compiler was built is then optimized.
 4. From this compiler, an **Algebricks Job** is created and then executed.

Given these assumptions, here is the suggested architecture (inspired from this paper [1]) :

![architecure](Asterix structure.png =270x200)

The sql++ compiler would provide an equivalent of the `APIFramework` class and would use a translator of type `SQLplusplusExpressionToPlanTranslator` to transform the input SQL++ query into an algebricks logical plan (of class `ILogicalPlan`).

Now the problem comes as follows : 

*I do not know what an `ILogicalPlan` should look like in order to be correctly optimized by the compiler. The documentation for the source code of the `ALogicalPlanImpl` class is very limited. I do not know either what is the normal form in which this plan should be, in order to have the compiler apply optimization rewriting rules properly.*

Now what I am looking for is whether :

 1. My understanding of the implementation is correct.
 2. A solution (or an idea for a solution) to the problem stated above.

Thank you very much,

Best,

\[1\]: *ASTERIX: An Open Source System for "Big Data" Management and Analysis*