## AstToPlan Visitor Implementation


### FLOWGR 

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
 
### Translate Query
 
 ```java
	/**
    This method translates an AQL Ast into an Algebricks Logical Plan.
    */
    public ILogicalPlan translate(Query expr) throws AlgebricksException, AsterixException {
    	/** 
        The visitor generates the Logical Plan, where the top operator is a project.
        */
        Pair<ILogicalOperator, LogicalVariable> p = expr.accept(this, new MutableObject<ILogicalOperator>(new EmptyTupleSourceOperator()));
        ArrayList<Mutable<ILogicalOperator>> globalPlanRoots = new ArrayList<Mutable<ILogicalOperator>>();
        ILogicalOperator topOp = p.first;
        // Top operator is a projection.
        ProjectOperator project = (ProjectOperator) topOp;
        // What's the difference between resVar and p.second?
        LogicalVariable resVar = project.getVariables().get(0);

		// What is outputDatasetName? I assume this is for the case where the output
        // of the query is inputed into some dataset.
        if (outputDatasetName == null) {
        	// ------Section-----
            // Not sure I understand this section. Why do we need to create an output
            // file?
            FileSplit outputFileSplit = metadataProvider.getOutputFile();
            if (outputFileSplit == null) {
                outputFileSplit = getDefaultOutputFileLocation();
            }
            metadataProvider.setOutputFile(outputFileSplit);
            // -------------------
            List<Mutable<ILogicalExpression>> writeExprList = new ArrayList<Mutable<ILogicalExpression>>(1);
            writeExprList.add(new MutableObject<ILogicalExpression>(new VariableReferenceExpression(resVar)));
            ResultSetSinkId rssId = new ResultSetSinkId(metadataProvider.getResultSetId());
            ResultSetDataSink sink = new ResultSetDataSink(rssId, null);
            topOp = new DistributeResultOperator(writeExprList, sink);
            topOp.getInputs().add(new MutableObject<ILogicalOperator>(project));
        } else {
            /** add the collection-to-sequence right before the final project, because dataset only accept non-collection records */
            LogicalVariable seqVar = context.newVar();
            @SuppressWarnings("unchecked")
            /** This assign adds a marker function collection-to-sequence: if the input is a singleton collection, unnest it; otherwise do nothing. */
            AssignOperator assignCollectionToSequence = new AssignOperator(seqVar,
                    new MutableObject<ILogicalExpression>(new ScalarFunctionCallExpression(
                            FunctionUtils.getFunctionInfo(AsterixBuiltinFunctions.COLLECTION_TO_SEQUENCE),
                            new MutableObject<ILogicalExpression>(new VariableReferenceExpression(resVar)))));
            assignCollectionToSequence.getInputs().add(
                    new MutableObject<ILogicalOperator>(project.getInputs().get(0).getValue()));
            project.getInputs().get(0).setValue(assignCollectionToSequence);
            project.getVariables().set(0, seqVar);
            resVar = seqVar;

            DatasetDataSource targetDatasource = validateDatasetInfo(metadataProvider, stmt.getDataverseName(),
                    stmt.getDatasetName());
            ArrayList<LogicalVariable> vars = new ArrayList<LogicalVariable>();
            ArrayList<Mutable<ILogicalExpression>> exprs = new ArrayList<Mutable<ILogicalExpression>>();
            List<Mutable<ILogicalExpression>> varRefsForLoading = new ArrayList<Mutable<ILogicalExpression>>();
            List<String> partitionKeys = DatasetUtils.getPartitioningKeys(targetDatasource.getDataset());
            for (String keyFieldName : partitionKeys) {
                prepareVarAndExpression(keyFieldName, resVar, vars, exprs, varRefsForLoading);
            }

            String additionalFilteringField = DatasetUtils.getFilterField(targetDatasource.getDataset());
            List<LogicalVariable> additionalFilteringVars = null;
            List<Mutable<ILogicalExpression>> additionalFilteringAssignExpressions = null;
            List<Mutable<ILogicalExpression>> additionalFilteringExpressions = null;
            AssignOperator additionalFilteringAssign = null;
            if (additionalFilteringField != null) {
                additionalFilteringVars = new ArrayList<LogicalVariable>();
                additionalFilteringAssignExpressions = new ArrayList<Mutable<ILogicalExpression>>();
                additionalFilteringExpressions = new ArrayList<Mutable<ILogicalExpression>>();

                prepareVarAndExpression(additionalFilteringField, resVar, additionalFilteringVars,
                        additionalFilteringAssignExpressions, additionalFilteringExpressions);

                additionalFilteringAssign = new AssignOperator(additionalFilteringVars,
                        additionalFilteringAssignExpressions);

            }

            AssignOperator assign = new AssignOperator(vars, exprs);

            if (additionalFilteringAssign != null) {
                additionalFilteringAssign.getInputs().add(new MutableObject<ILogicalOperator>(project));
                assign.getInputs().add(new MutableObject<ILogicalOperator>(additionalFilteringAssign));
            } else {
                assign.getInputs().add(new MutableObject<ILogicalOperator>(project));
            }

            Mutable<ILogicalExpression> varRef = new MutableObject<ILogicalExpression>(new VariableReferenceExpression(
                    resVar));
            ILogicalOperator leafOperator = null;

            switch (stmt.getKind()) {
                case INSERT: {
                    InsertDeleteOperator insertOp = new InsertDeleteOperator(targetDatasource, varRef,
                            varRefsForLoading, InsertDeleteOperator.Kind.INSERT, false);
                    insertOp.setAdditionalFilteringExpressions(additionalFilteringExpressions);
                    insertOp.getInputs().add(new MutableObject<ILogicalOperator>(assign));
                    leafOperator = new SinkOperator();
                    leafOperator.getInputs().add(new MutableObject<ILogicalOperator>(insertOp));
                    break;
                }
                case DELETE: {
                    InsertDeleteOperator deleteOp = new InsertDeleteOperator(targetDatasource, varRef,
                            varRefsForLoading, InsertDeleteOperator.Kind.DELETE, false);
                    deleteOp.setAdditionalFilteringExpressions(additionalFilteringExpressions);
                    deleteOp.getInputs().add(new MutableObject<ILogicalOperator>(assign));
                    leafOperator = new SinkOperator();
                    leafOperator.getInputs().add(new MutableObject<ILogicalOperator>(deleteOp));
                    break;
                }
                case CONNECT_FEED: {
                    InsertDeleteOperator insertOp = new InsertDeleteOperator(targetDatasource, varRef,
                            varRefsForLoading, InsertDeleteOperator.Kind.INSERT, false);
                    insertOp.setAdditionalFilteringExpressions(additionalFilteringExpressions);
                    insertOp.getInputs().add(new MutableObject<ILogicalOperator>(assign));
                    leafOperator = new SinkOperator();
                    leafOperator.getInputs().add(new MutableObject<ILogicalOperator>(insertOp));
                    break;
                }
            }
            topOp = leafOperator;
        }
        globalPlanRoots.add(new MutableObject<ILogicalOperator>(topOp));
        ILogicalPlan plan = new ALogicalPlanImpl(globalPlanRoots);
        return plan;
    }
```

 - Are all plans linear (or can we have operators with multiple children in the plan)?
 - What's the difference between resVar and p.second?
 - What is outputDatasetName?