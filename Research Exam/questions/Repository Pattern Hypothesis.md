## Web Service and GAV Mediator Hypothesis

The Web Service (and Repository Pattern) used for Polyglot Persistence in the industry. 
Once the choice is made that the application requires multiple coordinating data stores, it is the "standard" way to approach integration of multiple 

is nothing more than a manifestation of a Global-As-View mediator approach in a slightly different context from the 1990's.


 - Functions in repository pattern -> Views in GAV mediator.
 - Multiple databases with different query semantics ->
 - Updating the multiple database -> incremental view maintenance.

 
Need to verify :

#### Understand completely the two systems we want to show the equivalence for

 - Make sure exisiting definition of repository pattern is exhaustive.
 - Understanding how GAV systems update and retrieve data. Focus on correctness, performance does not matter for the moment

### w

 - Show that any retrieve function exposed by the repository module is is equivalent to a GAV view.
 - Show that the update function exposed by the repository module is equivalent to an update of a GAV view.