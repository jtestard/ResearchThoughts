## A Deep Embedding of Queries in Ruby

Created a rails plugin/software called Switch, which does the same job as Active Record but which much better performance, because it takes into account the application program structure when transalting application program statements into SQL queries.

#### Active Record

1) Concatenates clauses using a `ActiveRecord::Relation` object. Once all clauses have been concatenated, they have to be consumed.

Consumption of query clauses is triggered through the `map` method, or when statements completes). Examples :
   - `Order.group("user_id").having`

#### Switch

 - Derives expression over the ruby program while execution occurs, then compile program into SQL statements.

 
#### Questions 

 - What are the limits of the translation capabilities of switch?

### Understood

 - Switch is a DSL with its own type system and expressions.
 - Switch expressions are translated into ASTs which span multiple statements.
 - Switch values can be literals, tuples or ordered lists. Values which are not part of switch's runtime are evaluated and reduced to constants.
 - Execution of switch expression is deferred until elements are all consumed in the host language.
 - Switch iterations may happen in any order
 - They identify an iteration context using a position operator

The position operator is only used for internal logic