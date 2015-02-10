Ok,

So here is the conclusion of my meeting with Yingyi :

1) The metadata issue is not really an issue, rather an observation. If we really want to, it is possible to generate an Asterix Logical Plan from a SQL++ query without starting an Asterix instance. However, we will be using the SQL++ interface with an Asterix instance running, so we don’t really care.

2) We have to figure out what we want to do regarding how the users will interact with the SQL++ interface. We have two options :

First, the choices :

 a. We can opt to use a SQL++ syntax for all statements (DDL and DML).
 - We can opt to use SQL++ for queries only and use AQL for all other statement types.


Second, the facts :

 1. A single parser must be used for all statements in a given program. The solution that I described in the previous email involving using two parsers will be very hard to implement*. This means that if we opt for b) we will have no choice but copy over all of the parser code from the existing AQL parser to the SQL++ parser.
 2. The SQL++ Reference Implementation Parser (which is a cleaner parser being built by one of Yannis's Masters students) uses a parsing framework different from that of the existing AQL parser. Given 1), if we opt for b) and we want to use the new parser we won't be able to copy the parsing code from the exisiting AQL parser and have to reimplement everything using the new parsing framework.

Yingyi tells me he is fine with both options but we need to know which option we are going for ASAP since the choice will affect the software design.

\* : If you want more details why that is, just ask me.