## Friday December 18th Research Presentation

### Part 1: Refresher on rewritings

There are three rewritings:

 1. Semijoin rewriting (no requirement)
 - Normalized set rewriting (requires key for grouping) => duplicate elimination also possible
 - Denormalized set rewriting (requires key for grouping) => duplicate elimination also possible

We have two approaches rewritings 2) and 3):
 - using `PARTITION BY`
 - using semistructured `GROUP BY` (requires subquery on the groups)

We don't consider sources or execution engines for the moment.


### Part 2: Execution plans on Middleware and AsterixDB
