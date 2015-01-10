### Implementation plan

1. Move complex values from Value Type to Expression. Rename AbstractValue to AbstractLiteral.
- Add accept methods to expression and clauses of the SQLPP AST.
- Write methods of the SQLPPVistor stealing as much as possible from the AQL visitor.