## Discussion on AsterixDB changes

Classify into two types of issues

### Hyracks Issues

##### Unimplemented Visitors
Have not implemented some visitors for the OuterUnnestOperator because I was never using those visitors and leaving those implementations blank did not break any test cases.


**Yingyi**: Can the code be shared with the old UnnestOperator?
It looks most of the code is duplicated here.
Can you create an AbstractUnnestNonMapOperator as a parent class for these two?
Also, more importantly, you should override the method
public IVariableTypeEnvironment computeOutputTypeEnvironment(ITypingContext ctx) throws AlgebricksException
here in a similar fashion to the implementation in LeftOuterJoinOperator.
Because the variables produced by operator is nullable.

===============

Outer Unnest 
