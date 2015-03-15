# SQL++ Core Rewriting

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
ExprQuery       ===>         SelectElementClause
                                    |
                                ExprQuery
```