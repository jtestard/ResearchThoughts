# SQL++ Interface Documentation

## BNF for SQL++ Queries

####TOKENS

```
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<ASC: "asc">
| <AT: "at">
| <DATAVERSE: "dataverse">
| <DISTINCT: "distinct">
| <IN: "in">
| <LIMIT: "limit">
| <OFFSET: "offset">
| <UNION: "union">
| <WITH: "with">
| <USE: "use">
| <SELECT: "select">
| <FROM: "from">
| <WHERE: "where">
| <AS: "as">
| <JOIN: "join">
| <ON: "on">
| <INNER: "inner">
| <OUTER: "outer">
| <LEFT: "left">
| <RIGHT: "right">
| <FULL: "full">
| <MAP: "map">
| <HAVING: "having">
| <CORRELATE: "correlate">
| <ATTRIBUTE: "attribute">
| <GROUP: "group">
| <ELEMENT: "element">
| <FLATTEN: "flatten">
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<GROUP_BY: "group" (" ")* "by">
| <ORDER_BY: "order" (" ")* "by">
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<CARET: "^">
| <DIV: "/">
| <IDIV: "idiv">
| <MINUS: "-">
| <MOD: "%">
| <MUL: "*">
| <PLUS: "+">
| <LEFTPAREN: "(">
| <RIGHTPAREN: ")">
| <LEFTBRACKET: "[">
| <RIGHTBRACKET: "]">
| <LEFTARROW: "->">
| <RIGHTARROW: "<-">
| <SEMICOLON: ";">
| <COLON: ":">
| <COMMA: ",">
| <DOT: ".">
| <QUES: "?">
| <LT: "<">
| <GT: ">">
| <LE: "<=">
| <GE: ">=">
| <EQ: "=">
| <NE: "!=">
| <SIMILAR: "~=">
| <ASSIGN: ":=">
| <AND: "and">
| <OR: "or">
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<LEFTBRACE: "{"> : DEFAULT
}

   
<DEFAULT> TOKEN : {
<RIGHTBRACE: "}"> : {
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<LEFTDBLBRACE: "{{"> : IN_DBL_BRACE
}

   
<IN_DBL_BRACE> TOKEN : {
<RIGHTDBLBRACE: "}}"> : {
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<INTEGER_LITERAL: (<DIGIT>)+>
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<NULL: "null">
| <TRUE: "true">
| <FALSE: "false">
| <MISSING: "missing">
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<#DIGIT: ["0"-"9"]>
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<DOUBLE_LITERAL: <DIGITS> | <DIGITS> ("." <DIGITS>)? | "." <DIGITS>>
| <FLOAT_LITERAL: <DIGITS> ("f" | "F") | <DIGITS> ("." <DIGITS> ("f" | "F"))? | "." <DIGITS> ("f" | "F")>
| <DIGITS: (<DIGIT>)+>
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<#LETTER: ["A"-"Z","a"-"z"]>
| <SPECIALCHARS: ["$","_","-"]>
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<STRING_LITERAL: "\"" (<EscapeQuot> | <EscapeBslash> | <EscapeSlash> | <EscapeBspace> | <EscapeFormf> | <EscapeNl> | <EscapeCr> | <EscapeTab> | ~["\"","\\"])* "\"" | "\'" (<EscapeApos> | <EscapeBslash> | <EscapeSlash> | <EscapeBspace> | <EscapeFormf> | <EscapeNl> | <EscapeCr> | <EscapeTab> | ~["\'","\\"])* "\'">
| <#EscapeQuot: "\\\"">
| <#EscapeApos: "\\\'">
| <#EscapeBslash: "\\\\">
| <#EscapeSlash: "\\/">
| <#EscapeBspace: "\\b">
| <#EscapeFormf: "\\f">
| <#EscapeNl: "\\n">
| <#EscapeCr: "\\r">
| <#EscapeTab: "\\t">
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<IDENTIFIER: <LETTER> (<LETTER> | <DIGIT> | <SPECIALCHARS>)*>
}

   
<DEFAULT,IN_DBL_BRACE> TOKEN : {
<VARIABLE: "$" <LETTER> (<LETTER> | <DIGIT> | "_")*>
}

   
<DEFAULT,IN_DBL_BRACE> SKIP : {
" "
| "\t"
| "\r"
| "\n"
}

   
<DEFAULT,IN_DBL_BRACE> SKIP : {
<"//" (~["\n"])* "\n">
}

   
<DEFAULT,IN_DBL_BRACE> SKIP : {
<"//" (~["\n","\r"])* ("\n" | "\r" | "\r\n")?>
}

   
<DEFAULT,IN_DBL_BRACE> SKIP : {
"/*" : INSIDE_COMMENT
}

   
<INSIDE_COMMENT> SPECIAL : {
<"+" (" ")* (~["*"])*>
}

   
<INSIDE_COMMENT> SKIP : {
"/*" : {
}

   
<INSIDE_COMMENT> SKIP : {
"*/" : {
| <~[]>
}
```
   
####NON-TERMINALS

```
/**
 * SQL++ Statement Rules
 */
Statements  ::= ( SingleStatement <SEMICOLON> )* <EOF>
SingleStatement ::= ( DataverseDeclaration | Query )
/**
 * Imported from AQL
 */
DataverseDeclaration    ::= <USE> <DATAVERSE> AQLIdentifier
AQLIdentifier   ::= <IDENTIFIER>
|   AQLStringLiteral
AQLStringLiteral    ::= <STRING_LITERAL>
/*
 * =============================================================================================================================
 * Queries
 * =============================================================================================================================
 */
Query   ::= ( SfwQuery | ExprQuery )
/*
 * =============================================================================================================================
 * SFW Queries
 * =============================================================================================================================
 */
SfwQuery    ::= ( SfwQuerySelectFirst | SfwQuerySelectLast )
SfwQuerySelectFirst ::= SelectClause FromClause ( WhereClause )? ( GroupByClause )?
SfwQuerySelectLast  ::= FromClause ( WhereClause )? ( GroupByClause )? SelectClause
/*
 * =============================================================================================================================
 * FROM Clause
 * =============================================================================================================================
 */
FromClause  ::= <FROM> FromItem
FromItem    ::= ( ( FromSingle ( FromCorrelate )? ) | FromFlattenItem )
FromSingle  ::= ExprQuery <AS> FromVariables
FromVariables   ::= ( FromCollectionItem | FromTupleItem )
FromCollectionItem  ::= Variable ( <AT> Variable )?
FromTupleItem   ::= <LEFTBRACE> Variable <COLON> Variable <RIGHTBRACE>
FromCorrelate   ::= ( FromInnerCorrelateItem | FromLeftCorrelateItem | FromFullCorrelateItem | FromInnerJoin | FromLeftOuterJoin | FromFullOuterJoin | FromCartesianProduct )
FromInnerCorrelateItem  ::= <INNER> <CORRELATE> FromItem
FromCartesianProduct    ::= <COMMA> FromItem
FromLeftCorrelateItem   ::= <LEFT> ( <OUTER> )? <CORRELATE> FromItem
FromFullCorrelateItem   ::= <FULL> ( <OUTER> )? <CORRELATE> FromItem <ON> ExprQuery
FromInnerJoin   ::= ( <INNER> )? <JOIN> FromItem ( <ON> ExprQuery )?
FromLeftOuterJoin   ::= <LEFT> ( <OUTER> )? <JOIN> FromItem ( <ON> ExprQuery )?
FromFullOuterJoin   ::= <FULL> ( <OUTER> )? <JOIN> FromItem <ON> ExprQuery
FromFlattenItem ::= ( FromInnerFlatten | FromOuterFlatten )
FromInnerFlatten    ::= <INNER> <FLATTEN> <LEFTPAREN> ExprQuery <AS> Variable <COMMA> ExprQuery <AS> Variable <RIGHTPAREN>
FromOuterFlatten    ::= <OUTER> <FLATTEN> <LEFTPAREN> ExprQuery <AS> Variable <COMMA> ExprQuery <AS> Variable <RIGHTPAREN>
/*
 * =============================================================================================================================
 * WHERE Clause
 * =============================================================================================================================
 */
WhereClause ::= <WHERE> ExprQuery
/*
 * =============================================================================================================================
 * GROUP BY Clause
 * =============================================================================================================================
 */
GroupByClause   ::= <GROUP_BY> GroupByItem ( GroupByItem )*
GroupByItem ::= ExprQuery <AS> Variable
/*
 * =============================================================================================================================
 * SELECT Clause
 * =============================================================================================================================
 */
SelectClause    ::= <SELECT> ( SelectElementClause | SelectAttributeClause | SelectTupleClause )
SelectElementClause ::= <ELEMENT> ExprQuery
SelectAttributeClause   ::= <ATTRIBUTE> ExprQuery <COLON> ExprQuery
SelectTupleClause   ::= ( ( ExprQuery ( <AS> StringValue )? ) ( ( <COMMA> ExprQuery ( <AS> StringValue )? ) )* )
/*
 * =============================================================================================================================
 * Expr Queries
 * =============================================================================================================================
 */
ExprQuery   ::= ( OperationQuery )
NestedQuery ::= <LEFTPAREN> SfwQuery <RIGHTPAREN>
OperationQuery  ::= RelationshipQuery ( <EQ> RelationshipQuery )?
RelationshipQuery   ::= ( ValueQuery ) ( NavStep )*
NavStep ::= ( TupleNav | ArrayNav )
TupleNav    ::= <DOT> ( Identifier | StringValue )
ArrayNav    ::= <LEFTBRACKET> ExprQuery <RIGHTBRACKET>
ValueQuery  ::= ( Variable | Value | Dataset | NestedQuery )
Identifier  ::= <IDENTIFIER>
Variable    ::= ( <VARIABLE> )
Dataset ::= <IDENTIFIER>
/*
 * =============================================================================================================================
 * Values
 * =============================================================================================================================
 */
Value   ::= ( MissingValue | NullValue | ComplexValue | ScalarValue )
MissingValue    ::= <MISSING>
NullValue   ::= <NULL>
ComplexValue    ::= ( TupleValue | CollectionValue )
TupleValue  ::= ( ( <LEFTBRACE> <RIGHTBRACE> ) | ( <LEFTBRACE> ( Identifier | StringValue ) <COLON> ExprQuery ( <COMMA> ( Identifier | StringValue ) <COLON> ExprQuery )* <RIGHTBRACE> ) )
CollectionValue ::= ( ArrayValue | BagValue )
ArrayValue  ::= ( ( <LEFTBRACKET> <RIGHTBRACKET> ) | ( <LEFTBRACKET> ExprQuery ( <COMMA> ExprQuery )* <RIGHTBRACKET> ) )
BagValue    ::= ( ( <LEFTDBLBRACE> <RIGHTDBLBRACE> ) | ( <LEFTDBLBRACE> ExprQuery ( <COMMA> ExprQuery )* <RIGHTDBLBRACE> ) )
ScalarValue ::= PrimitiveValue
PrimitiveValue  ::= ( NumberValue | StringValue | BooleanValue )
NumberValue ::= ( <INTEGER_LITERAL> | <FLOAT_LITERAL> | <DOUBLE_LITERAL> )
StringValue ::= <STRING_LITERAL>
BooleanValue ::= ( <TRUE> | <FALSE> )
``` 

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
