# Use Cases for Rewriting

 1. **ETL workflow** : workflow loads data into a system which supports/desires nesting (such as MongoDB, Asterix...), for operational intelligence purposes.
 -  **BDAS (Big Data Analytics System)** : used by business intelligence users to develop insight over their data (Hive, Asterix ...). This is the use case targeted by TPC-DS and TPC-BB benchmarks.
 -  **Analytics Visualization** : application which provides analytics visuals for a browser, which consumes PL-friendly data.
 -  **Online Rest API** : online web service which provides information to be consumed by external services, such as mobile applications or other web services.

### Systems Considered

 - **Hadoop ETL**: ETL workflow software orchestrating a Hadoop-based system (example: Informatica BDM solution). Can be used in single node or multi-node configuration.
 - **Hive** : can be used in single node or multi-node configuration. Given Hadoop ETLs will typically generate Hive Jobs, both share the same cost model.
 - **FORWARD Middleware**
 - **AsterixDB** : can be used in single node or multi-node configuration.


### Characteristics of use cases for rewriting
 
| Use Case 	| Consumer 	| System 	| Levels Of Nesting 	| Query Reach* 	| Result Size 	| Use of Top-k  	| Query latency 	| Multi-node Query** 	| Benchmarks 	|
|-------------------------	|------------------------------------------------------------------------------	|-----------------	|----------------------	|--------------	|-------------	|---------------	|---------------	|--------------------	|----------------	|
| ETL Workflow 	| Operational Intelligence (storing log data, building pre-aggregated reports) 	| Hadoop ETL 	| 1+ levels of nesting 	| large 	| large 	| Maybe 	| Long-running 	| Yes 	| ? 	|
| BDAS 	| Business Intelligence Users producing reports over large quantities of data 	| Hive, AsterixDB 	| 0+ levels of nesting 	| large 	| small 	| Yes 	| Long-running 	| Yes 	| TPC-DS, TPC-BB 	|
| Analytics Visualization 	| Web application server-side code interacting with database 	| Forward 	| 1+ levels of nesting 	| small 	| small 	| Yes 	| Short 	| No 	| ? 	|
| Online Rest API 	| Mobile and Web applications 	| AsterixDB 	| 1+ levels of nesting 	| small 	| small 	| Maybe 	| Short 	| No 	| ? 	|

 - \*: amount of data that *must* be read in order to answer a query accurately
 - \**: assumes data is somewhat localized. Yes if query is likely to require data from multiple nodes despite localization [No if not].