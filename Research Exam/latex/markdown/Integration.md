Approach :

 - Have one section per challenge cited in the introduction.
 - For each section, have a list of relevant papers and compare their approach.
 - For now, no need to restructure the sections. 
 - For integration, show the different components :
   - federated architecture
   - common data model
   - unifiying query language
   - procedural vs declarative approach

#### Federated MiddleWare Architecture

 - Most PP systems that have been studied focus on middle ware based architecture in which the user specifies a query which is then translated into sub components.
 - Each sub component corresponding to a fragment which is sent to individual subsystems.
 - These fragments are then translated into the subsystem's native query language and executed on those subsystems.
 - The results of the fragment queries are then returned to the middleware which joins them together to form a response to the user initial query.
 - This technique is inherited from the classical data integration integration problem that has been studied extensively in the 1990's.
 - **We describe here this classical approach**.
 - however, builders of PP systems are confronted to a problem which global as view systems did not have to deal with.
 - GAV mediators were using the relational model as a unifying model to represent all data.
 - heterogeneity of data models. Some data models fit very badly within the relational model.
 - Fitting such data into relational views becomes quite complicated.
 - People have come up with solutions and we detail them here.

 

 
Integrating Data From Multiple Sources : Historical Review
 