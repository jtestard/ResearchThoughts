## Attribute Grammar for SQL++ Abstract Syntax Tree (AST) to Asterix Logical Plan Translation

This document shows the attribute grammar specification of the translation process from SQL++ ASTs to Asterix Logical Plans.
The terminology used should be familiar to anyone having studied attribute grammars but if you haven't, here is a [link](http://homepage.cs.uiowa.edu/~slonnegr/plf/Book/Chapter3.pdf)
to a very good tutorial. Intuitively, this grammar describes a parser which "parses" syntax trees and "produces" logical plans. The naming conventions are described here :

##### Non-Terminals
Each materialized `non-terminal` symbol is either an Asterix Operator **or** an Asterix Expression. A third category of non-terminals (prepended with an `_` symbol) are used for intermediate results and are eventually not materialized in the output. 

##### Terminals
Each `'terminal'` symbol is a node from a SQL++ AST. Terminal symbols can be distinguished by the use of `''` around them. 

##### Aliases
Each symbol (terminal or not) may have an `{alias}` . Aliases can be distinguished by the use of `{}` around them. Aliases are handy when describing attributes.

##### Attributes
As in any attribute grammar, non-terminals may have attributes. Attribute `attr` for non-terminal `expression` is written as `expression.attr`. Attributes can be assigned to a value this way : `expression.attr <- value`. In this attribute grammar, we classify attributes into three categories : properties, logical variables and tuple sources.

###### Properties
These attributes represent properties of the Asterix expressions/operators. Their name and role should be familiar to anyone with knowledge of the Asterix Logical Plan structure (if not, now is a good time to learn :smiley: ). These attributes are always synthesized.

###### Logical Variables
Logical Variables are Asterix constructs which are neither operators nor expressions, but appear in both to refer to information computed by child operators. They are uniquely identified by an integer id. The id of a variable is expressed this way : `variable.id`. There are two ways to create a variable : 

 - Using the context constructor : `context.NewVar()`
 - Using the id of a SQL++ AST Variable node : `context.newVar(var)`

These attributes are always synthesized.

###### Operator Input
This attribute is present in all materialized operators. It specifies the order in which operators are executed (an operator executes after its input has finished executing). This attribute are always inherited (except for the `DistributeResultOperator` which is the top most operator and cannot inherit).

##### Production Description
Each production is accompanied by a description of the role of the left hand side non-terminal in Asterix and what its attributes represent.

##### Start Symbol
The start symbol for this attribute grammar is the `DistributeResultOperator`.

##### Visualization
Finally, the visualization of what the left hand side non-terminal would look like on the Asterix Web Interface is provided.    

### Productions

#### DistributeResultOperator

```
DistributeResultOperator{dro}           ::= ProjectOperator{po}
                               Attributes : dro.input <- po
                                            dro.variable <- po.variable
                                            po.isTop <- true
```
The `DistributeResultOperator` is the top-most operator in every plan. In the attribute grammar, it possesses two attributes : the `input` (see operator input above) and the `variable`. The `DistributeResultOperator` is visualized as :

```
distribute result [%0->$$0]
``` 

where `variable.id = 0`. This operator does not play a role until further in the Asterix processing pipeline. 

#### ProjectOperator

```
ProjectOperator{p}                     ::=  'SfwQuery'{sfwq}
                                          /         |       \
                       _SelectClause{sc}    _FromClause{fc} (_WhereClause{wc})?
                               condition  : sfwq.isTop = true
                               Attributes : p.variable <- sc.variable
                                            fc.input <- empty-tuple-source
                                            if wc exists then
                                                wc.input <- fc
                                                sc.input <- wc
                                            else
                                                sc.input <- fc
                                            p.input <- sc
```

The `ProjectOperator` specifies which Logical Variable should be output to the eventual end-user.
In the attribute grammar, it possesses two attributes :

 - The `input` (see operator input above).
 - The `variable` which specifies what the end-user will see as output.

The `ProjectOperator` is visualized as :

```
project [$$0]
``` 

where `variable.id = 0`.

#### AssignOperator

```
_SelectClause{sc}                      ::=  AssignOperator{a}
                                    Attributes : sc <- a.input
AssignOperator{a}                       ::= _SelectElementExpression{see}
                               Attributes : a.expression <- see
                                            a.variable <- context.newVar()
                                            see.input <- a.input
                                        |   _SelectTupleExpression{ste}
                               Attributes : a.expression <- ste
                                            a.variable <- context.newVar()
                                            ste.input <- a.input
```

In Asterix, the `AssignOperator` is used to assign an Asterix Expression to a new Logical Variable.
In the attribute grammar, it has three attributes :

 - the `expression` (the expression to assign).
 - the `variable` (the variable the expression will be assigned to).
 - the `intput` (see operator input above).
 
It is visualized as :

```
assign $$0 <- expression
```

where `variable.id = 0`.

#### SelectElementExpression

```
_SelectElementExpression{see}          ::=  'SelectElementClause'
                                                    |
                                        _SQLPPExpression{sqlppe}
                                    Attributes : see <- sqlppe
```
Intermediate result.

#### SelectTupleExpression

```
_SelectTupleExpression{ste}        ::=  'SelectTupleClause'
                                                |
                                 ScalarFunctionCallExpression{sfce}
                                Attributes : ste <- sfce
```

#### SQLPPExpression

```
_SQLPPExpression{sqlppe}                ::= ScalarFunctionCallExpression{sfce}
                                    Attributes: sqlppe <- sfce
                                        |   VariableReferenceExpression{vre} 
                                    Attributes: sqlppe <- vre
                                        |   _NestedQueryExpression{nqe}
                                    Attributes: sqlppe <- nqe
```
Intermediate result.

#### SubplanOperator

```
_NestedQueryExpression{nqe}             ::= SubplanOperator{spo}
                                    Attributes : spo <- nqe
SubPlanOperator{spo}                    ::= 'NestedQuery'{nq}
                                                |
                                         AggregateOperator{agg}
                                    Attributes : spo.rootOp <- agg
                                                
```
In the attribute grammar, the `SubPlanOperator` has two attributes :

 - The `input` (see input operator description above).
 - The `rootOp` is the root operator of the subplan operator.   

The `SubPlanOperator` is visualized as :

```
subplan {
    ...
}
```

#### AggregateOperator

```
AggregateOperator{agg}                  ::=    'SfwQuery'{sfwq}
                                          /         |       \
                       _SelectClause{sc}    _FromClause{fc} (_WhereClause{wc})?
                               condition  : sfwq.isTop = false
                               Attributes : agg.variable <- context.newVar()
                                            agg.listVariable <- sc.variable
                                            fc.input <- nested-tuple-source
                                            wc.input <- fc
                                            sc.input <- wc
                                            agg.input <- sc
```
In Asterix, the `AggregateOperator` is used as the top level elements of subplans.
In our context, the `AggregateOperator` is used in conjunction with the `listify` asterix function which accumulates results from a subplan and passes the resulting list to the parent operator.  
In the attribute grammar, the `AggregateOperator` has three attributes :

 - The `input` (see input operator description above).
 - The `listVariable` (the variable which is used to accumulate tuples from the subplan).
 - The `variable` (the variable which is assigned the output of the aggregation). 
 
The `AggregateOperator` is visualized as :

```
aggregate [$$1] <- [function-call: asterix: listify, Args: [%0-$$1]]
```
where `listVariable.id=0` and `variable.id = 1`.

#### FromClause

```
_FromClause{fc}                     ::=   'FromClause'
                                                |
                                            _FromItem{fi}
                                Attributes : fc <- fi
                                
_FromItem{fi}                       ::=  _FromCollectionItem{fci}
                                Attributes : fi <- fci
                                    |    _FromInnerCorrelateItem{fici}
                                Attributes : fi <- fici
                                    |    _FromInnerJoinItem{fiji}
                                Attributes : fi <- fiji
                                 
_FromCollectionItem{fci}            ::= UnnestOperator{unnest}
                                Attributes : fci <- unnest
                                
_FromInnerCorrelateItem{fici}       ::= 'FromInnerCorrelate'
                                        /               \
                         _FromCollectionItem{fci1}  _FromCollectionItem{fci2}
                                Attributes : fic1.input <- fci2
                                             fic2.input <- fici.input

_FromInnerJoinItem{fiji}            ::=     'FromInnerJoinItem'
                                        /               |         \
              _FromCollectionItem{fci1}  _FromCollectionItem{fci2} SelectOperator{so}
                                Attributes : so.input <- fic1
                                             fci1.input <- fic2
                                             fci2.input <- fiji.input
```

#### UnnestOperator

```
UnnestOperator{op}                     ::=  'FromCollectionItem'
                                            /        |          \
        UnnestingFunctionCallExpression{unnest}  'Variable'{e}  'Variable'{p}
                                Attributes : op.unnestExpression <- unnest
                                    op.variable <- context.newVar(e)
                                    op.positionalVariable <- context.newVar(p)
                                    unnest.input <- op.input
```

In Asterix, the `UnnestOperator` is used to unnest collections or datasets.
In the attribute grammar, it has four attributes : 
 - the `unnestExpression`.
 - the `variable` which stores the unnesting output for each new binding tuple.
 - the `positionalVariable` which stores the index of each new binding tuple (if the output of the unnest is ordered).
 - the `input` (see operator input above).
 
The `UnnestOperator` is visualized as :

```
unnest $$0 at $$1 <- unnestExpression
```

where `variable.id = 0` and `positionalVariable.id = 1`.


#### UnnestingFunctionCallExpression

```
UnnestingFunctionCallExpression{unnest} ::= _SQLPPExpression{sqlppe}
                                   Attributes : unnest.functionId <- scan-collection
                                                unnest.expression <- sqlppe
                                                sqlppe.input <- unnest.input
                                        |   _DatasetFunctionCallExpression{dsfce}  
                                   Attributes : unnest.functionId <- scan-dataset
                                                unnest.expression <- dsfce
                                                sqlppe.input <- unnest.input
```

In Asterix, the `UnnestingFunctionCallExpression` is an expression which specifies the behavior of an `UnnestOperator`.
In the attribute grammar, the `UnnestingFunctionCallExpression` has two attributes : the `functionId` and the `expression`.

 - The `expression` is the Asterix Expression which will be unnested.
 - The `functionId` describes how the unnest operator will proceed to scan the contents of the expression during the evaluation. Its value can be `scan-dataset` (for expressions which evaluate to dataset names) or `scan-collection` (for expression which evaluate to unordered lists (bags) and ordered lists (arrays)).  

The `UnnestingFunctionCallExpression` is visualized as :

```
function-call: asterix:scan-collection, Args:[expression]   if functionId = scan-collection
function-call: asterix:scan-dataset, Args[expression]       if functionId = scan-dataset
```

#### SelectOperator

```
_WhereClause{wc}            ::=  'WhereClause'
                                       |
                               SelectOperator{so}
                        Attributes : wc <- so
SelectOperator{so}          ::=  _SQLPPExpression{sqlppe}
                             sqlppe.input <- so 
```
The `SelectOperator` in Asterix filters its input binding tuples according to a condition expression.
In the attribute grammar, it has only one attribute, the `input` (see operator input above).
The `SelectOperator` is visualized as :

```
select [expression]
```

#### DatasetFunctionCallExpression

```
_DatasetFunctionCallExpression{dsfce}    ::=  'FunctionCall'
                                             /           \
                                  'StringValue'{type}   'List<Query>'{args}
                                                            |
                                                        ConstantExpression{dsName}
                                   condition : type = "dataset"
                                   Attributes : dsfce <- dsName
                                                dsName.input <- dsfce.input
```
Intermediate result. This production only applies if the condition `type = "dataset"` is met. 

#### ConstantExpression

```
ConstantExpression{const}               ::= 'StringValue'{str}
                                   Attributes : const.value = str
                                        |   'NumberValue'{num}
                                   Attributes : const.value = num
                                        |   'BooleanValue'{bool}
                                   Attributes : const.value = bool 
```

The `ConstantExpression` is used in Asterix to represent constants. In the attribute grammar, it has a single attribute called `value` which represents the value of the constant. 
The `ConstantExpression` is visualized as :

```
AString: {value}        if value is a string
AInt: {value}           if value is a number
ABool: {value}          if value is a boolean  
```

#### VariableReferenceExpression

```
VariableReferenceExpression{vre}        ::= 'Variable'{var}
                                    Attributes : vre.variable = context.newVar(var)
```

A `VariableReferenceExpression` is used in Asterix to represent references to variables (the variable must already exist). In the attribute grammar, it has a single attribute called `variable` which represents the variable referenced. The `VariableReferenceExpression` is visualized as :

```
%0 -> $$0 
```

where `variable.id = 0`.
 
#### ScalarFunctionCallExpression

```
ScalarFunctionCallExpression{sfce}          ::= _NavigationExpression{ne}
                                        Attributes : sfce <- ne
                                            |   _BinaryOperationExpression{boe}
                                        Attributes : sfce <- boe
                                            |   _ComplexValueConstructExpr{cvce}
                                        Attributes : sfce <- cvce
                                            |   _SelectTupleItems{sti}
                                        Attributes : sfce <- sti
```

The roles of the `ScalarFunctionCallExpression`s in Asterix range from navigation to arithmetic operations to complex value construction.
The `ScalarFunctionCallExpression`'s versatility comes from the wide range of function identifiers it can be configured with.
In the attribute grammar, it has two attributes :

  - The `functionId` which represents the function identifier associated with the expression.
  - The `arguments` which represents the list of arguments for the function. 

The `ScalarFunctionCallExpression` is visualized as :

```
function-call: asterix: functionId, Args[arguments] 
```

The production is split into intermediate results for better readability.  

#### NavigationExpression

```
_NavigationExpression{ne}               ::= 'FunctionCall'
                                            /           \
                                  'StringValue'{type}   'List<Query>'{args}
                                                          /         \
                                      _SQLPPExpression{sqlppe}   'StringValue'{nav}
                                    condition:  type = "tuple_nav"
                                    Attributes: ne.functionId <- field-acces-by-name
                                                ne.arguments[0] <- sqlppe
                                                ne.arguments[1] <- nav
                                                sqlppe.input <- ne.input
                                        |   'FunctionCall'
                                            /           \
                                  'StringValue'{type}   'List<Query>'{args}
                                                          /         \
                                      _SQLPPExpression{sqlppe}   'StringValue'{nav}
                                    condition:  type = "array_nav"
                                    Attributes: ne.functionId <- get-item
                                                ne.arguments[0] <- sqlppe
                                                ne.arguments[1] <- nav
                                                sqlppe.input <- ne.input
```

#### BinaryOperationExpression
```
_BinaryOperationExpression{boe}       ::=  'FunctionCall'
                                            /           \
                                  'StringValue'{type}   'List<Query>'{args}
                                                          /         \
                                      _SQLPPExpression{sqlpp1}   _SQLPPExpression{sqlpp2}
                                    condition:  type = "and"
                                    Attributes: boe.functionId <- and
                                                boe.arguments[0] <- sqlpp1
                                                boe.arguments[1] <- sqlpp2
                                                sqlpp1.input <- boe.input
                                                sqlpp2.input <- boe.input
                                        |  'FunctionCall'
                                            /           \
                                  'StringValue'{type}   'List<Query>'{args}
                                                          /         \
                                      _SQLPPExpression{sqlpp1}   _SQLPPExpression{sqlpp2}
                                    condition:  type = "eq"
                                    Attributes: boe.functionId <- eq
                                                boe.arguments[0] <- sqlpp1
                                                boe.arguments[1] <- sqlpp2
                                                sqlpp1.input <- boe.input
                                                sqlpp2.input <- boe.input
```

#### ComplexValueConstructionExpression

```
_ComplexValueConstructExpr{cvce} ::=    'TupleValue'
                                              |
                                     'Map<String, ExprQuery>'
                                   /          |         \
                         Pair1               ...             PairN
                    /            \                      /               \
'StringValue'{alias1}   _SQLPPExpression{sqlpp1} 'StringValue'{aliasN}   _SQLPPExpression{sqlppN}
      Attributes: cvce.functionId <- open-record-constructor
          cvce.arguments[0] <- alias1
          cvce.arguments[1] <- sqlpp1
          ...
          cvce.arguments[2n-2] <- aliasN
          cvce.arguments[2n-1] <- sqlppN
          sqlpp1.input <- cvce.input
          ...
          sqlppN.input <- cvce.input
                                    |   'BagValue'
                                            |
                                   'HashSet<ExprQuery>'
                                 /          |          \
               _SQLPPExpression{sqlpp1}    ...    _SQLPPExpression{sqlpp1}
      Attributes: cvce.functionId <- unordered-list-constructor
          cvce.arguments[0] <- sqlpp1
          ...
          cvce.arguments[n-1] <- sqlppN
          sqlpp1.input <- cvce.input
          ...
          sqlppN.input <- cvce.input
                                    |   'ArrayValue'
                                            |
                                   'ArrayList<ExprQuery>'
                                 /          |          \
               _SQLPPExpression{sqlpp1}    ...    _SQLPPExpression{sqlpp1}
      Attributes: cvce.functionId <- ordered-list-constructor
          cvce.arguments[0] <- sqlpp1
          ...
          cvce.arguments[n-1] <- sqlppN
          sqlpp1.input <- cvce.input
          ...
          sqlppN.input <- cvce.input
```


#### SelectTupleItems

```
_SelectTupleItems{sti}            ::=  _SelectTupleItems
                                              |
                                          'ItemList'
                                   /          |         \
                      SelectItem             ...           SelectItem
                    /            \                      /               \
'StringValue'{alias1}   _SQLPPExpression{sqlpp1} 'StringValue'{aliasN}   _SQLPPExpression{sqlppN}
      Attributes: sti.functionId <- open-record-constructor
          sti.arguments[0] <- alias1
          sti.arguments[1] <- sqlpp1
          ...
          sti.arguments[2n-2] <- aliasN
          sti.arguments[2n-1] <- sqlppN
          sqlpp1.input <- cvce.input
          ...
          sqlppN.input <- cvce.input
```

### Examples 

SQL++ AST :
```
SFW [
  From
      FunctionCall dataset[
        "FacebookUsers"
      ]
       as 
      fb[0][newVar]
      
     inner correlate 
       (
        SFW [
          From
            FunctionCall dataset[
              "FacebookMessages"
            ]
             as 
            fbm[1][newVar]
            
          Where
            FunctionCall eq[
              FunctionCall tuple_nav[
                fb[0][reference]
                "id"
              ]
              FunctionCall tuple_nav[
                fbm[1][reference]
                "author-id"
              ]
            ]
          
          Select Element
            fbm[1][reference]
          
        ]
      )
       as 
      fbm[2][newVar]
      
    
  Where
    FunctionCall eq[
      FunctionCall tuple_nav[
        fb[0][reference]
        "id"
      ]
      1
    ]
  
  Select Element
    TupleValue [
      (
      name
        :
      FunctionCall tuple_nav[
        fb[0][reference]
        "name"
      ]
      )
      (
      fbm
        :
      FunctionCall tuple_nav[
        fbm[1][reference]
        "message"
      ]
      )
    ]
  
]
```

Resulting Plan : 

```
distribute result [%0->$$11]
  project ([$$11])
    assign [$$11] <- [function-call: asterix:open-record-constructor, Args:[AString: {name}, function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {name}], AString: {fbm}, function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {message}]]]
      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], AInt32: {1}])
        unnest $$2 <- function-call: asterix:scan-collection, Args:[%0->$$8]
          subplan {
                    aggregate [$$8] <- [function-call: asterix:listify, Args:[%0->$$1]]
                      select (function-call: algebricks:eq, Args:[function-call: asterix:field-access-by-name, Args:[%0->$$0, AString: {id}], function-call: asterix:field-access-by-name, Args:[%0->$$1, AString: {author-id}]])
                        unnest $$1 <- function-call: asterix:dataset, Args:[AString: {FacebookMessages}]
                          nested tuple source
                 }
            unnest $$0 <- function-call: asterix:dataset, Args:[AString: {FacebookUsers}]
              empty-tuple-source
```
