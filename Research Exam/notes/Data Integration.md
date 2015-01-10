# Data Integration

## Slides from doan, halevy and ives


### Goal of data integration

 - Tie together different data sources that may have been created indepently by many people, and put them under a global schema.
 - Uniform accesss to set of data sources.
 - Challenges :
   - Scalability
   - Availability
   - Data model variety (semi-structured vs fully structured data)
   

### Data Integration Abstraction

 - Queries are made according to the global schema.
 - The global schema is semantically mapped to the schema of each datasource. Individual sources may have different data models, syntax and semantics. The global schema must thus be able to express the semantics of all sources.
 
### Data Integration Applications

 - Business
 - Science
 - Government
 - Web
 - other


#### Business Applications

 - A large business has a number of :
   - Entreprise Data Sources (Core Logic)
   - Legacy Data Sources
   - Archive Data Sources
   - Backup Data Sources
   - Loggig Data Sources
   - more ...

#### Science Applications

- A science lab may have :
   - Phenotype data
   - Genome Data
   - DNA data (Nucleotide sequences)
   - Sensor Data
   - Geographical Data
   - Medical data ...

#### Web Applications

The slides are out of date when it comes to web...

### Data Heterogeneity

Example of two databases with different schema. Poses the question of schema mapping.

### Data Integration Reasons

Some of the reasons presented in this 

 - Serving SOA data.
 - Collaborating with third parties.
 - Comply with government regulations?
 - Business Intelligence.

### Why is it hard?

System :
 - querying accross multiple systems.
 - optimize query execution across multiple systems.
 - handling transactions across multiple systems.
 - distributed query processing (handling failures).
Theory-level :
 - Schema and data heterogeneity