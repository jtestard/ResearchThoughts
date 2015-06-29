We have seen that Forward provides an interface to interact with the different data stores. But some problems still remain :

 - Forward does not help the user partition his data. 
 - Forward does not help the user decide in which data store each partition should be stored.

We can see through this example (show example) that the data partitioning we chose earlier is not the best if we consider only the running example query.

Say we change our data partitioning to this (show new 

If we decided to change our data partitioning we could get a much higher performance for the running example query. 