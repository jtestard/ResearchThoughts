# AsterixDB Wrapper Implementation

## Goals

The goals of the AsterixDB wrapper have been described in the form of test cases in a presentation available here : 

	/Users/julestestard/Projects/svn/forward/trunk/doc/Internal Presentations/2014-10-16 SQL++ AsterixDB Use Cases.pptx

The goal would be to have the Forward query processor cover all of these cases. We will attempt to cover problems starts from the earliest example to the latest. It would be great that for this purpose we use the [yelp data set](http://www.yelp.com/dataset_challenge).

## Implementation steps
We are working from an implementation standpoint. This means that while we may attempt to follow the query specification, if there is a conflict between the specification and the implementation, the implementation will take precedence.

### Forward Plan Identification
We first want to identify plans that are emitted by the query processor. It was decided to go with a package named `edu.ucsd.forward.query.source_wrapper.asterix`.

### Send a fixed AQL query to AsterixDB from Forward
We test if we can send a query of the following form to the Asterix DB cluster.

	let $message := 'Hello World!'
    return $message
### Notes

 - The overwrite field has no effect yet.
 - We use AQL for insertion of data and schema.
 - To implement the data model, I have chosen to go with importing the AsterixDB-OM jar.
 - Data model.

### Assumptions

 - We lazily implement features for the wrapper (any method not used by the test will throw a unimplemented exception).
 - We assume the data source has only one properties field (properties tags beyond the first will be ignored).

### Errors found

 - In JDBC data source, port is never checked for.

--------------------
### Notes

#### Forward Query Compiler Test Case
 1. create java source class.
 2. create package under `src/test/java` with an appropriate package name (e.g. `edu.ucsd.forward.asterix.query.ast`).
 	- Inside this package, create Java classes for your test cases. Follow the conventions from the classes in neighbour packages for annotations and such.
 3. create package under `src/test/resources` (no Util) with identical package name.
    - Inside this package, put your XML resource files. 
    
### TODO

 - fix svn 1.6 seg fault.
 - process of creating test cases. 
 
 Process of creating a test case for the Forward Query Compiler in (using testNG)