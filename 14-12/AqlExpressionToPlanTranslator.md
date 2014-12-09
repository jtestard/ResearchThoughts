In this section, we explore a function from the AqlExpressionToPlanTranslator and detail our understanding of the behaviour of that function through the code and debugger.

@Override    
    public Pair<ILogicalOperator, LogicalVariable> visitFlworExpression(FLWOGRExpression	        Mutable<ILogicalOperator> tupSource) throws AsterixExce	        Mutable<ILogicalOperator> flworPlan = tupSou
ce;

                boolean isTop = context.isTopFlwor();
        if (isTop) {
            context.setTopFlwor(false);
        }
        for (Clause c : flwor.getClauseList()) {
            Pair<ILogicalOperator, LogicalVariable> pC = c.accept(this, flworPlan);
            flworPlan = new MutableObject<ILogicalOperator>(pC.first);
        }

        Expression r = flwor.getReturnExpr();
        boolean noFlworClause = flwor.noForClause();

        if (r.getKind() == Kind.VARIABLE_EXPRESSION) {
            VariableExpr v = (VariableExpr) r;
            LogicalVariable var = context.getVar(v.getVar().getId());

            return produceFlwrResult(noFlworClause, isTop, flworPlan, var);

        } else {
            Mutable<ILogicalOperator> baseOp = new MutableObject<ILogicalOperator>(flworPlan.getValue());
            Pair<ILogicalOperator, LogicalVariable> rRes = r.accept(this, baseOp);
            ILogicalOperator rOp = rRes.first;
            ILogicalOperator resOp;
            if (expressionNeedsNoNesting(r)) {
                baseOp.setValue(flworPlan.getValue());
                resOp = rOp;
            } else {
                SubplanOperator s = new SubplanOperator(rOp);
                s.getInputs().add(flworPlan);
                resOp = s;
                baseOp.setValue(new NestedTupleSourceOperator(new MutableObject<ILogicalOperator>(s)));
            }
            Mutable<ILogicalOperator> resOpRef = new MutableObject<ILogicalOperator>(resOp);
            return produceFlwrResult(noFlworClause, isTop, resOpRef, rRes.second);
        }
    }
