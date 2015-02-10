## Tests for SQL++ Parser

 - `AND` and `OR` connectors in operator expression.
 - Relationship expressions (`<`, `=`, ...) 
 - `+` , `-` expressions.
 - `*` , `/` , `%` , `^`, `idiv` expressions.
 - signed expressions `-82`, `+46`, `45`.
 - `.id` tuple access expression.
 - `[2]` array access expression.
 - `->("hi")` map access expression.
 - `LiteralExpression` (all of `IntValue`, `DoubleValue`, `StringValue` ...)
 - `EnrichedValueExpression`
 - `From` clause.
 - `Select` clause.
 - `Where` clause.
 
 
Goal : We express SQL++ SFW queries without

 - Position variables.
 - Nested Subqueries.
 - Group By queries.
 - Set operators.
 - Syntactic sugar.
 - Flatten.
 - Function calls (other than operators from OperatorExpression)
 - Quantified expressions
  
  
 The AQL query class has been changed to the AQLQuery class and now implements the Query interface (located in AQL base). Both SQLPPQuery and AQLQuery classes implement that interface.
 
 There is something fishy with the QueryLanguage.