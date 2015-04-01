### Traces


#### 

#### CancelUnnestWithNestedListifyRule

These traces follow the debugger in order to understand better how a rewrite rule works.

We first trace the `CancelUnnestWithNestedListifyRule`.


```
    private boolean applies(Mutable<ILogicalOperator> opRef, Set<LogicalVariable> varUsedAbove,
            IOptimizationContext context) throws AlgebricksException {
        AbstractLogicalOperator op1 = (AbstractLogicalOperator) opRef.getValue();
        if (op1.getOperatorTag() != LogicalOperatorTag.UNNEST) {
            return false;
        }
        UnnestOperator unnest1 = (UnnestOperator) op1;

>> unnest1 = unnest [$$2] <- function-call: asterix:scan-collection, Args:[%0->$$7]

        ILogicalExpression expr = unnest1.getExpressionRef().getValue();

>> expr = function-call: asterix:scan-collection, Args:[%0->$$7]

        LogicalVariable unnestedVar;
        switch (expr.getExpressionTag()) {
            case VARIABLE:
                unnestedVar = ((VariableReferenceExpression) expr).getVariableReference();
                break;
                
>> Won't happen
                
            case FUNCTION_CALL:
                if (((AbstractFunctionCallExpression) expr).getFunctionIdentifier() != AsterixBuiltinFunctions.SCAN_COLLECTION) {
                    return false;
                }
                AbstractFunctionCallExpression functionCall = (AbstractFunctionCallExpression) expr;
                ILogicalExpression functionCallArgExpr = functionCall.getArguments().get(0).getValue();
                
>> functionCallArgExpr : %0->$$7
                
                if (functionCallArgExpr.getExpressionTag() != LogicalExpressionTag.VARIABLE) {
                    return false;
                }
                unnestedVar = ((VariableReferenceExpression) functionCallArgExpr).getVariableReference();
                
>> unnestedVar : $$7

                break;
            default:
                return false;
        }
        if (varUsedAbove.contains(unnestedVar)) {
        
>> varUsedAbove : [$$0, $$2, $$8]
// not sure why this condition is put here.
        
            return false;
        }

        Mutable<ILogicalOperator> opRef2 = op1.getInputs().get(0);
        
>> opRef2 : SubplanOperator
        
        AbstractLogicalOperator r = (AbstractLogicalOperator) opRef2.getValue();

        if (r.getOperatorTag() != LogicalOperatorTag.GROUP) {
            return false;
        }

        // go inside of a group-by plan
        GroupByOperator gby = (GroupByOperator) r;
        if (gby.getNestedPlans().size() != 1) {
            return false;
        }
        if (gby.getNestedPlans().get(0).getRoots().size() != 1) {
            return false;
        }

        AbstractLogicalOperator nestedPlanRoot = (AbstractLogicalOperator) gby.getNestedPlans().get(0).getRoots()
                .get(0).getValue();
        if (nestedPlanRoot.getOperatorTag() != LogicalOperatorTag.AGGREGATE) {
            return false;
        }
        AggregateOperator agg = (AggregateOperator) nestedPlanRoot;
        Mutable<ILogicalOperator> aggInputOpRef = agg.getInputs().get(0);

        if (agg.getVariables().size() > 1) {
            return false;
        }

        LogicalVariable aggVar = agg.getVariables().get(0);
        ILogicalExpression aggFun = agg.getExpressions().get(0).getValue();
        if (!aggVar.equals(unnestedVar)
                || ((AbstractLogicalExpression) aggFun).getExpressionTag() != LogicalExpressionTag.FUNCTION_CALL) {
            return false;
        }
        AbstractFunctionCallExpression f = (AbstractFunctionCallExpression) aggFun;
        if (!AsterixBuiltinFunctions.LISTIFY.equals(f.getFunctionIdentifier())) {
            return false;
        }
        if (f.getArguments().size() != 1) {
            return false;
        }
        ILogicalExpression arg0 = f.getArguments().get(0).getValue();
        if (((AbstractLogicalExpression) arg0).getExpressionTag() != LogicalExpressionTag.VARIABLE) {
            return false;
        }
        LogicalVariable paramVar = ((VariableReferenceExpression) arg0).getVariableReference();

        ArrayList<LogicalVariable> assgnVars = new ArrayList<LogicalVariable>(1);
        assgnVars.add(unnest1.getVariable());
        ArrayList<Mutable<ILogicalExpression>> assgnExprs = new ArrayList<Mutable<ILogicalExpression>>(1);
        assgnExprs.add(new MutableObject<ILogicalExpression>(new VariableReferenceExpression(paramVar)));
        AssignOperator assign = new AssignOperator(assgnVars, assgnExprs);

        LogicalVariable posVar = unnest1.getPositionalVariable();
        if (posVar == null) {
            // Creates assignment for group-by keys.
            ArrayList<LogicalVariable> gbyKeyAssgnVars = new ArrayList<LogicalVariable>();
            ArrayList<Mutable<ILogicalExpression>> gbyKeyAssgnExprs = new ArrayList<Mutable<ILogicalExpression>>();
            for (int i = 0; i < gby.getGroupByList().size(); i++) {
                if (gby.getGroupByList().get(i).first != null) {
                    gbyKeyAssgnVars.add(gby.getGroupByList().get(i).first);
                    gbyKeyAssgnExprs.add(gby.getGroupByList().get(i).second);
                }
            }

            // Moves the nested pipeline before aggregation out of the group-by op.
            Mutable<ILogicalOperator> bottomOpRef = aggInputOpRef;
            AbstractLogicalOperator bottomOp = (AbstractLogicalOperator) bottomOpRef.getValue();
            while (bottomOp.getOperatorTag() != LogicalOperatorTag.NESTEDTUPLESOURCE) {
                bottomOpRef = bottomOp.getInputs().get(0);
                bottomOp = (AbstractLogicalOperator) bottomOpRef.getValue();
            }

            // Removes the group-by operator.
            opRef.setValue(assign);
            assign.getInputs().add(aggInputOpRef);
            AssignOperator gbyKeyAssign = new AssignOperator(gbyKeyAssgnVars, gbyKeyAssgnExprs);
            gbyKeyAssign.getInputs().add(gby.getInputs().get(0));
            bottomOpRef.setValue(gbyKeyAssign);

            context.computeAndSetTypeEnvironmentForOperator(gbyKeyAssign);
            context.computeAndSetTypeEnvironmentForOperator(assign);
        } else {
            // if positional variable is used in unnest, the unnest will be pushed into the group-by as a running-aggregate

            // First create assign for the unnest variable
            List<LogicalVariable> nestedAssignVars = new ArrayList<LogicalVariable>();
            List<Mutable<ILogicalExpression>> nestedAssignExprs = new ArrayList<Mutable<ILogicalExpression>>();
            nestedAssignVars.add(unnest1.getVariable());
            nestedAssignExprs.add(new MutableObject<ILogicalExpression>(arg0));
            AssignOperator nestedAssign = new AssignOperator(nestedAssignVars, nestedAssignExprs);
            nestedAssign.getInputs().add(opRef2);

            // Then create running aggregation for the positional variable
            List<LogicalVariable> raggVars = new ArrayList<LogicalVariable>();
            List<Mutable<ILogicalExpression>> raggExprs = new ArrayList<Mutable<ILogicalExpression>>();
            raggVars.add(posVar);
            StatefulFunctionCallExpression fce = new StatefulFunctionCallExpression(
                    FunctionUtils.getFunctionInfo(AsterixBuiltinFunctions.TID), UnpartitionedPropertyComputer.INSTANCE);
            raggExprs.add(new MutableObject<ILogicalExpression>(fce));
            RunningAggregateOperator raggOp = new RunningAggregateOperator(raggVars, raggExprs);
            raggOp.setExecutionMode(unnest1.getExecutionMode());
            RunningAggregatePOperator raggPOp = new RunningAggregatePOperator();
            raggOp.setPhysicalOperator(raggPOp);
            raggOp.getInputs().add(nestedPlanRoot.getInputs().get(0));
            gby.getNestedPlans().get(0).getRoots().set(0, new MutableObject<ILogicalOperator>(raggOp));

            opRef.setValue(nestedAssign);

            context.computeAndSetTypeEnvironmentForOperator(nestedAssign);
            context.computeAndSetTypeEnvironmentForOperator(raggOp);
            context.computeAndSetTypeEnvironmentForOperator(gby);

        }

        return true;
    }
```