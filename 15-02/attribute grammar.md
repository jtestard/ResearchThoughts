## Attribute Grammar for AST to Plan Translation

We describe the SQL++ AST to Asterix Logical Plan Translation using an attribute grammar `G(N,T,P)` such that :

 - `N` is the set of non-terminals of `G` where `N` is the set of `Asterix Operators` unioned with the set of  `Asterix Expressions`.
 - `T` is the set of terminals of `G` where `T` is the set of Extended SQL++ AST nodes. 
 - `P` is the set of production rules of the grammar.

#### Tokens

Same as non-terminals from SQL++ Queries BNF. 

#### Non-Terminals

Some observations :
 - In order to distinguish identically named non-terminals in the left hand side of productions, subscripts are added of the form `<X>` where `X` identifies that non-terminal in the context of the production.
 - We create the `value()` function which retrieves the value of the attribute of a SQL++ AST node terminal. This value can then be used in attributes of non-terminals.
 - We.

```
Plan                ::= ProjectOperator

ProjectOperator     ::=  'SfwQuery' 

AssignOperator      ::=

SelectOperator      ::=

AggregateOperator   ::=

UnNestOperator      ::=             'FromCollectionItem'
                                  /          |          \
                        UnNestExpression LogicalVar<E> LogicalVar<P>
UnNestExpression.tupSource <- UnNestOperator.tupSource
UnNestOperator.elementVar <- context.newVar(LogicalVar<E>.id)
UnNestOperator.positionVar <- context.newVar(LogicalVar<P>.id)
UnNestOperator.variable <- UnNestOperator.elementVar

UnNestExpression    ::=   'FunctionCall[Dataset]'
                                   |
                              ConstantExpr
UnNestExpression.fid = 'dataset'
UnNestExpression.fid = 'scan_collection'
                    |     'FunctionCall[

ConstantExpr        ::= 'StringValue'
                    |   'BooleanValue'
                    |   'NumberValue'
                    |   'NullValue'

TupSource           ::= EmptyTupleSource
                    |   UnNestOperator
                    |   AssignOperator
                    |   SubPlanOperator
                    |   NestedTupleSource
                    |   SelectOperator
                    
sqlppToAlgExpr      ::=                     

ScalarCallExpr      ::=

ConstantExpression  ::=

VarRefExpression    ::=

ComplexValueCall    ::= OpenRecordExpression
                    |   BagCaExpression
                    |   ArrayCallExpression 

TupleCallExpression ::= 

BagCallExpression   ::=

ArrayCallExpression ::= 

FieldAccessByName   ::=

GetItemCallExpr     ::=

OpenRecordCallExpr  ::= 'SelectTupleClause' SelectTupleItem

SelectTupleItem     ::= 

LogicalVar          ::= 'Variable' 
                        id = value('Variable.id')

EmptyTupleSource    ::= ''

NestedTupleSource   ::= ''

```