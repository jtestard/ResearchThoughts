# Amazon Task Notes

Amazon EMR is a facility which allows easy setup of Hadoop clusters over EC2 instances.

### Task Description

#### Frameworks/Technologies to familiarize myself with:

 - Elastic Map Reduce (EMR)
 - Spark and SparkSQL
 - S3
 - AWS Data Pipeline
 - Schema-lift (I added that one myself): I was able to read the Amiato description, but I was wondering if there is a paper which describes the technique more thoroughly; seems related to part 2 of the project.

#### Scenario Task:

 - Collect wikipedia edits and load them onto Redshift, using Amazon platform for ETL using EMR and/or SparkSQL. 
 - Make a short summary over the difficulties encountered (1 page, I know no one will read anything longer than that), positioning myself as a potential customer of the product.
 - I will let you know as soon as the scenario task is complete.

#### Additional Notes

 - One problem with this plan is that EMR is not part of the AWS free tier.
 - I plan to follow this tutorial to get started with the scenario task (creates a EMR cluster using spark, loading data from S3) : http://aws.amazon.com/articles/Elastic-MapReduce/4926593393724923.
 - One way we could tackle this problem is by simply having me completing the task and then file a reimbursement.
 - Charges should be small, given the smallest cluster costs $0.011/hour and I won’t need it for more than a few hours. 

### Services Used

 - Amazon EMR
 - Amazon EC2
 - Amazon S3

## Tutorial #1 : Getting Started: Analyzing Big Data with Amazon EMR

 - Create AWS Bucket : **done**
 - Create AWS Key-Pair : **done**
 - Done using default configurations. Billing will be `0.266 * 3 * HoursUsed`.
 - Present data and scripts using S3 urls:
   - http://us-west-2.elasticmapreduce.samples.s3.amazonaws.com/ for data

## Tutorial #2 : Apache Spark on EMR

 - Describes configuration options for Apache Spark on EMR. We will not be using any special configuration options.

### Creating and accessing spark cluster

 - EMR has a quickstart which allows bootstrapping a spark cluster.
 - the spark cluster itself will create EC2 instances, security groups, and appropriate roles.
 - the aws cli is configured with a user which has AmazonElasticMapReduceRole and AmazonElasticMapReduceforEC2Role roles.
 - EC2 master needs to be configured for SSH access by modifying the master security group. This will be required for every new instance.

### Accessing the spark shell

 - Accessing the spark shell requires an SSH connection.
 - Spark shell can be used 

## Scenario Task

 - Loaded Wiki pages as XML files onto S3.
 - XML Schema is available.

**Sub-tasks**:

 - Write a local, "dumbed-down" version on my own machine, using local spark + postgresql.
 - Write a pyspark script which load data from S3 into Redshift
 - Write a AWS pipeline workflow which does the same
 - Write a report describing the experience

### Spark SQL

 - Data frames vs Data Sets: we ignore data sets for now. 

In both cases, we need to define a schema to use on top of redshift.
Once the schema is defined we need to load the data.

### Operations Notes :

 - 


### Log the difficulties encountered

 - Loading data file. Takes time?
 - You need a good schema for your input, we are lucky we already have both DTD and XSD.
   - Even when you have a target schema, it may be that the source and target schema don't match, in particular in terms of required fields.
     - My solution to this problem is to provide default values.
   - 
 - We need JDBC connection through spark
 - We need to manually decompose hierarchical data into row-based data to fit into redshift.
 - We need to manually parallelize data?
 - Loading based on early exploration, start with a small portion of the data set, will have problems when it scales.
 - Missing part of the structure, need multiple iterations
 - Manually unnest to connect with JDBC type.
 - Semi-structured data 
 - Schema knowledge
 - Dealing with wrappers/ capabilities 4pm
 - `java.sql.SQLFeatureNotSupportedException: [Amazon][JDBC](10220) Driver not capable.`
 - Dataframes with missing attributes will not fill them in, which throws off the redshift jdbc driver.

Decompressing is a problem, because the input data file is huge and the user has to write code which both decompress and parallelizes the task.

### Report notes

 - 1 page max
 - Bullet Point problems encountered
 - Make a calendar of time spent to accomplish each task. 

Decompress





