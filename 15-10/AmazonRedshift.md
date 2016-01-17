## Amazon Redshift

Amazon Redshift is a data warehouse cluster which looks like a relational database.

There is :

 - One leader node : this node interacts with clients. When only one node is present, a leader node is not necessary (the single compute node acts as leader)
 - One or more compute nodes : 