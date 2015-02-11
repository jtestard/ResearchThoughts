# SQL++ Interface Documentation

You can refer to the BNF for SQL++ Queries [here](SQL++BNF.md)

## Rewriting Rules for SQL++ AST

All the rules given below are applied in a one-pass bottom-up algorithm.

### Reduction to SQL++ Core

The following rules allow to transform non-core SQL++ constructs into their core equivalent. When the algorithm visits the root of the tree on the left side, it transforms that tree into the tree on the right side using the appropriate rule.

##### FromCartesianProduct Rule

```
		FromCartesian						FromInnerCorrelate
		/			\           ===>		/	              \
	FromItemL	FromItemR				FromItemL            FromItemR
```

##### FromInnerFlatten Rule

```
      FromInnerFlatten                       FromInnerCorrelate
        /           \           ===>        /                 \
    FromItemL   FromItemR               FromItemL            FromItemR
```

##### FromOuterFlatten Rule

```
      FromOuterFlatten                     FromLeftCorrelate
        /           \           ===>        /              \
    FromItemL   FromItemR               FromItemL         FromItemR
```

##### SelectTuple Rule

```
        SelectTupleClause                              SelectElement
                |                                           |
             ItemList                ===>               TupleValue
       /        |        \                                  |
 SelectItem1   ...     SelectItemN                      attributes
    /       \           /      \                      /     |      \
 Expr1  alias1        ExprN   aliasN             Pair1    ...      PairN
                                               /      \          /       \
                                            Expr1  alias1      ExprN  aliasN
                                            value1   key1      valueN  keyN
```

where :
 
  - `Expr` is an `ExprQuery`.
  - `alias` is a `StringValue`.
  - `itemList` is a `List<SelectItem>`.
  - `attributes` is a `Map<String, ExprQuery>`.

##### InnerJoin rule

```
             InnerJoinItem                            InnerCorrelate
         /          |            \        ===>         /          \
 FromItemL FromCollectionItemR Condition         FromItemL     newFromCollectionItemR
            /       |                                         /             \
         Expr   oldElemVar                               NestedQuery     newElemVar
                                                             /
                                                        SfwQuery
                                                   /       |         \
                                    SelectElementClause FromClause    WhereClause
                                          /                |                \
                                     oldElemVar   FromCollectionItemR    Condition
                                                    /      |
                                                 Expr   oldElemVar                                  
```

where :

 - `Expr` and `Condition` are `ExprQuery`s.
 - `oldElemVar` and `newElemVar` are `Variable`s.

**Observations** :

 - The `LeftOuterJoinItem` rewriting rule is identical but uses a `LeftCorrelateItem` as the root of the right tree instead.
 - The right item of the Inner Join is assumed to be a `FromCollectionItem`. Handling other types of `FromItem` expressions is still in development. 


#### Other AST Nodes

When the algorithm visits a tree whose root type does not match one of the types above, the identity rule is used instead. Here is an example of the identity rule for the `FromClause` :

```
FromClause          FromClause
    |       ===>        |
 FromItem            FromItem
```

#### Note

The `Order By` and `Group By` clause being not fully supported for the moment, rewriting rules for those constructs (if any?) are not included.

### Other Rewritings

#### Top-level Expression Queries

This rewriting is independent from the Core Reduction rewriting and occurs before the Core Reduction. If the top-level expression is not a `SfwQuery` it is transformed into one as follows :

```
ExprQuery       ===>         SfwQuery
                           /          \
                 SelectElementClause  FromClause
                        |                  |
                   Variable             FromCollectionItem
                                        /           \
                                  ExprQuery        Variable                                
```

## AST to Plan Translation Productions

Work in progress. Will be transformed into an attribute grammar where :

 - The set of non-terminals is the set of `Asterix Operators` unioned with the set of  `Asterix Expressions`.
 - The set of terminals is the set of Extended SQL++ AST nodes.

##### FromCollectionItem

###### Dataset Input
```
         FromCollectionItem             ===>    unnest $$0 <- function-call: asterix:dataset, Args:[
       /          |         \                                                       AString: {DatasetName}
 FunctionCall ElementVar PositionVar                                                 ]
 {'Dataset'}     id=0       null
     |
[Arg0='DatasetName']
```

Note that Datasets are bags (position variabls cannot be used).

###### Variable Input
```
         FromCollectionItem             ===>    unnest $$0 at $$1 <- function-call: asterix:scan-collection, Args:[%0->$$2]
       /          |         \                                                       
 Variable   ElementVar PositionVar                                                 
   id=2       id=0       id=1
```

###### Tuple/Array Navigation Input
```
         FromCollectionItem             ===>    unnest $$0 at $$ 1 <- function-call: asterix:scan-collection, Args:[
       /          |         \                                   function-call: asterix:field-access-by-name, Args:[
 FunctionCall ElementVar PositionVar                                         %0 -> $$2,
 {'TupleNav'}    id=0       id=1                                            AString: {AttributeName}
     |                                                                  ]
[Arg0=ExprQuery,Arg1='AttributeName']
        id=2
```

if the result of `ExprQuery` is in variable with id `2`.

###### Nested Query Input
```
         FromCollectionItem             ===>    unnest $$0 at $$ 1 <- function-call: asterix:scan-collection, Args:[%0->$$2]
       /          |         \                                                       
 NestedQuery  ElementVar PositionVar                                                 
   id=2         id=0       id=1
```

if the result of `NestedQuery` is in variable with id `2`.

#### FromInnerCorrelateItem

###### Two FromSingle
```
        FromInnerCorrelateItem              ===>  unnest $$1 <- ...
        /                 \                         unnested $$0 <- ...
 FromCollectionItemL    FromCollectionItemR
     id=0                   id=1
```

###### One FromSingle and One FromBinary

```
        FromInnerCorrelateItem              ===>  ( output from FromBinaryR ) 
        /                 \                         unnested $$0 <- ...
 FromCollectionItemL    FromBinaryR
     id=0                   
```

#### FromInnerJoinItem

Part of SQL++ Extended Translation.

```
             FromInnerJoin                  ===>    select ( Condition )
    /               |            \                      unnest $$1 <- ...
FromCollectionL FromCollectionR  Condition                  unnest $$0 <- ...
   id=0              id=1      
```

where `Condition` is an `ExprQuery`. 

FromBinary are not yet allowed within `FromInnerJoin`.

#### Binary Operators

###### Equality
```
    FunctionCall                ===>        function-call: algebricks:eq, Args[ Expr1, Expr2 ]
    {'Equality'}
         |
 [Arg0=Expr1, Arg1=Expr2]
```

###### And
```
    FunctionCall                ===>        function-call: algebricks:eq, Args[ Expr1, Expr2 ]
      {'and'}
         |
 [Arg0=Expr1, Arg1=Expr2]
```

#### Select Element

###### Tuple Value Element
```
      SelectElementClause            ===>     assign $$0 <- [function-call: asterix:open-record-constructor, Args:[
              |                                 AString: {alias1},
          TupleValue                            Expr1,
              |                                 ...
           Attributes                           AString: {aliasN},
     /        |       \                         ExprN
     Pair1   ...      PairN                     ]
   /      \          /       \
Expr1  alias1      ExprN  aliasN
value1   key1      valueN  keyN
```

###### Bag/Array Value Element
```
    SelectElementClause             ===>    assign $$0 <- [function-call: asterix:unordered-list-constructor, Args[
            |                                   Expr1
         BagValue                               ...
            |                                   ExprN
          values                                ]
       /    |    \
   Exrp1   ...  ExprN
```

##### Variable Element

```
    SelectElementClause             ===>    assign $$0 <- $$1
            |
         Variable
          id=0
```


Note, in practice the assign operator does not appear in the plan.

#### Select Tuple

```
        SelectTupleClause               ===>     assign $$0 <- [function-call: asterix:open-record-constructor, Args:[       
                |                                   AString: {alias1},
             ItemList                               Expr1,
       /        |        \                          ...
 SelectItem1   ...     SelectItemN                  AString: {aliasN},
    /       \           /      \                    ExprN
 Expr1  alias1        ExprN   aliasN                ]
```

#### SfwQuery

```
              SfwQuery              ===>        project [$$K+1]
         /         |        \                     assign $$K+1 <- ( expression from SelectClause )
SelectClause FromClause WhereClause                 select ( Condition)
                   |        |                         unnest $$K <- (expression from FromItem)  
                FromItem  Condition                    ...
                                                        unnest $$0 <- (expression from FromItem)
                                                          empty-tuple-source
```

#### NestedQuery

```
                                             subplan
             NestedQuery            ===>        aggregate [$$K+2] <- [function-call: asterix:listify, Args[%0 <- $$K+1]]
                  |                                 assign $$K+1 <- ( expression from SelectClause )
              SfwQuery                                select ( Condition )
         /         |        \                           unnest $$K <- ( expression from FromItem )
SelectClause FromClause WhereClause                      ...
                   |        |                             unnest $$0 <- ( expression from FromItem )
                FromItem  Condition                        empty-tuple-source
```
