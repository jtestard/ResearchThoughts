## AstToPlan Visitor Implementation

In this section, we explore a function from the AqlExpressionToPlanTranslator and detail our understanding of the behaviour of that function through the code and debugger.

```java
@Override    
public Pair<ILogicalOperator, LogicalVariable> visitFlworExpression(FLWOGRExpression flwor, Mutable<ILogicalOperator> tupSource) throws AsterixException {
    /*
    The output of each visit is a pair containing a logical operator and a logical variable. It is expected the operator output is bound to that variable. The input of the visit consists of an expression (in this case, FLWOGR) and an "input" logical operator.  
    */
	Mutable<ILogicalOperator> flworPlan = tupSource; //tup source should be Ground or some nested FLWOGR.
    boolean isTop = context.isTopFlwor();
    if (isTop) {
        context.setTopFlwor(false);
    } // Not sure what TopFlwor() is for.
    
	// The flowerPlan operator is tentatively put on top of the tuple source.
    // The order of the clauses will determine the eventual order of the operators.
    for (Clause c : flwor.getClauseList()) {
        //Each clause is visited and uses the output operator of the previous clause as input
        Pair<ILogicalOperator, LogicalVariable> pC = c.accept(this, flworPlan);
        flworPlan = new MutableObject<ILogicalOperator>(pC.first);
    } // Create a variable/operator binding for each clause of the FLWOGR expression.
    
    // At this point, it is assumed that all clauses have been added to the plan (except for the return clause).
    // -------------------------------------------------------
    
    Expression r = flwor.getReturnExpr(); 
    boolean noFlworClause = flwor.noForClause(); //Not sure what noFlworClause is for. 

    if (r.getKind() == Kind.VARIABLE_EXPRESSION) {
	   // Transform AST variable expressions into LogicalPlan variables.
       VariableExpr v = (VariableExpr) r;
       LogicalVariable var = context.getVar(v.getVar().getId());
       // Build project operator and assign output to var.
       return produceFlwrResult(noFlworClause, isTop, flworPlan, var);
    } else {
       Mutable<ILogicalOperator> baseOp = new MutableObject<ILogicalOperator>(flworPlan.getValue());
       // return is more complex than a variable, the output has to be assigned to subelements of the return expression.
       Pair<ILogicalOperator, LogicalVariable> rRes = r.accept(this, baseOp);
       // is rRes necessarily an assign operator?
       ILogicalOperator rOp = rRes.first;
       ILogicalOperator resOp;
       if (expressionNeedsNoNesting(r)) {
           baseOp.setValue(flworPlan.getValue());
           resOp = rOp;
       } else {
           // I do not understand this section very well. 
           SubplanOperator s = new SubplanOperator(rOp);
           s.getInputs().add(flworPlan);
           resOp = s;
           baseOp.setValue(new NestedTupleSourceOperator(new MutableObject<ILogicalOperator>(s)));
       }
       Mutable<ILogicalOperator> resOpRef = new MutableObject<ILogicalOperator>(resOp);
       // 
       return produceFlwrResult(noFlworClause, isTop, resOpRef, rRes.second);
   }
}
```

 - What is the `current op`?
 - What is `top flwor`? (crude understanding)
 - How are variable handled in context?
 - is rRes necessarily an assign operator?
 