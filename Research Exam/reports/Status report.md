### Status report

Our goals are to :

 1. Describe why the polyglot persistence problems has emerged.
   - Done through the defintion in the question log.
 - Describe why the polyglot persistence problem matters. Find a number of use cases which can convince the audience.
   - We got some of the use cases :
     - Streaming Processing (Cyclops)
     - Multi-pattern data access (Martin Fowler)
     - Realtime and Batch (Lambda Architecture)
 - Define formally the polyglot persistence problem.
    - This is hard to do as the term still is a little too broad. Various manifestations (or use cases) can be more formally described. It is probably to do a taxonomy the way it is done in the Answering Queries using Views paper).
 - Describe the challenges the polyglot persistence problem creates.
   - Some challenges have already been described in the progress report. There are some parallels between use cases and challenges. Not all uses cases care most about the same challenges : for example adaptive stream QP does not care so much about inter-database integrity. Need to map challenges to use cases through a use-case vs challenge matrix. 
 - For each challenge, describe the solutions found so far if they exist. If more than one solution exist for any given problems, compare the tradeoffs between solutions.
   - Haven't really attacked that part yet.
 - Present some of your own research/ideas.
   - It is my opinion that for at least the Multi-Pattern Data Access use case, and concerning querying only (and not updating) the proposed architecture is equivalent to that of a Global-As-View mediator.


Presentation to Yannis tomorrow :

Come up with a mini-presentation in case the discussion heads that way but don't necessarily show it. 