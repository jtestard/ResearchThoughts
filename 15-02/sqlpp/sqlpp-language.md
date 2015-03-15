# The SQL++ query language for Asterix

## Introduction

This document is intended as a reference guide to the full syntax and semantics of the SQL++ Query Language for Asterix (Asterix SQL++). This document describes how the SQL++ query language is parsed in the context of AsterixDB. Details for the SQL++ query language being developed at UCSD can be found [here](http://forward.ucsd.edu/.html).

It is important to note that while we are using the SQL++ query language, we are keeping the Asterix Data Model. As such, there will be some differences between the language presented here and the SQL++ Reference Implementation [1]. These differences will be clearly highlighted when they occur and will be kept at a minimum.

Note that the SQL++ interface currently only offers query capabilities. To do any sort of data (or metadata) manipulation, the regular AQL interface must be used. The language is presented using a BNF form.

### Statements

```
Statement       ::= ( SingleStatement ( ";" )? )* <EOF>
SingleStatement ::= DataverseDeclaration
                  | SQLPPQuery
```

For details about the `DataverseDeclaration` statement, please refer to the guide found [here](https://asterixdb.ics.uci.edu/documentation/aql/manual.html).

### Dataverse Declaration

```
DataverseDeclaration    ::= <USE> <DATAVERSE> AQLIdentifier
AQLIdentifier   ::= <IDENTIFIER>   |   AQLStringLiteral
AQLStringLiteral    ::= <STRING_LITERAL>
```

This is imported from AQL.

### Expressions
```
SQLPPQuery   ::= ( SfwQuery | ExprQuery )
```    
A SQL++ query can be an Expression query or a Select-From-Where query.

### SQL++ Select-From-Where Query

```
SfwQuery    ::= ( SfwQuerySelectFirst | SfwQuerySelectLast )
SfwQuerySelectFirst ::= SelectClause FromClause ( WhereClause )? ( GroupByClause )? (OrderByClause)?
SfwQuerySelectLast  ::= FromClause ( WhereClause )? ( GroupByClause )? SelectClause
```

A Select-From

### Order By Clause 

```
OrderByClause = <ORDER_BY> OrderByItem (, OrderByItem)* (LimitClause)? (OffsetClause)?
OrderByItem = 
```

####

### SQL++ Expression Query

```
OperatorExpression   ::= AndExpression ( "or" AndExpression )*
AndExpression        ::= RelExpression ( "and" RelExpression )*
RelExpression        ::= AddExpression ( ( "<" | ">" | "<=" | 
                         ">=" | "=" | "!=" | "~=" ) AddExpression )?
AddExpression        ::= MultExpression ( ( "+" | "-" ) MultExpression )*
MultExpression       ::= UnaryExpression ( ( "*" | "/" | "%" |
                         "^"| "idiv" ) UnaryExpression )*
UnaryExpression      ::= ( ( "+" | "-" ) )? ValueExpression
```

The operator expression structure is inherited from the AQL `OperatorExpression`.

#### SQL++ PathStep

```
ValueExpression  ::= PrimaryExpression (pathstep)*
Pathstep         ::= "." Identifier
                 |   "[" OperatorExpression "]"
                 |   "->(" OperatorExpression ")"
```
Notice that SQL++ does not have the "I am lucky" array navigation AQL has (the "?" in array navigation).

#### SQL++ Value Expression

```
PrimaryExpression ::=   Value
                  |     ParenthesizedExpression # Currently not supported
                  |     Variable
```
                    
#### SQL++ Literals

```
Value           ::=  DefinedValue
                |    "missing"
DefinedValue    ::=  ScalarValue
                |    ComplexValue
ScalarValue     ::=  PrimitiveValue
                |    EnrichedValue
PrimitiveValue   ::=  StringValue
                |    NumberValue
                |    "true"
                |    "false"
                |    "null"
NumberValue    ::=   IntegerValue
                |    FloatValue
                |    DoubleValue
EnrichedValue  ::=   Identifier "(" PrimitiveValue 
                     ( "," PrimitiveValue ) ? ")"
```
    
This section is inspired by the SQL++ Value BNF presented in [1]. However, some features from the BNF are not included. For example :

 - the `id::` field for defined values is absent from this specification. 
 - In order to map more closely to AQL primitives, the number value is subdivided further to its AQL equivalents.

#### SQL++ Complex Values

```
ComplexValue    ::=  TupleValue
                |    BagValue
                |    ArrayValue
                |    MapValue
TupleValue     ::=   "{" ( FieldBinding ( "," FieldBinding )* )?  "}"
BagValue       ::=   "{{" ( OperatorExpression ( "," OperatorExpression )* )?  "}}"
ArrayValue     ::=   "[" ( OperatorExpression ( "," OperatorExpression )* )?  "]"
MapValue       ::=   "map" "(" (Value ":" DefinedValue 
                     ( "," Value ":" DefinedValue )* )? ")" # not supported yet (ever)?
FieldBinding   ::=   OperatorExpression ":" OperatorExpression
```
Given that the Asterix Data Model does not contain maps, the usage of maps will be 
identified, but will also reported a "operation not supported" error.

#### SQL++ Parenthesized Expression

```
ParenthesizedExpression ::= "(" SFWExpression ")"
```

#### SQL++ Named Value and variables

```
DatasetExpression ::= Identifier
Variable   ::= Identifier
```

In a SQL++ query, it is not possible to distinguish a variable from a dataset expression without context. *Note that the concept of dataset expression replaces the named value expression existing in the SQL++ Reference Implementation.* (May need to verify)

### SQL++ SFWExpression

```
SFWExpression ::=   "SELECT" SelectClause
              |     "SELECT"  "DISTINCT" SelectClause
              |    "FROM" FromClause
              |    "WHERE" OperatorExpression
              |    "GROUPBY" GroupItem # Not supported yet
              |    "HAVING" OperatorExpression # Not supported yet
              |    ("UNION" | "INTERSECT" | "EXCEPT") ["ALL"] SFWExpression # Not supported yet
              |    "ORDER BY" OrderItem # Not supported yet
              |    "LIMIT" OperatorExpression # Not supported yet
              |    "OFFSET" OperatorExpression # Not supported yet
```

#### SQL++ Select Clause

```
SelectClause   ::= SelectItem (, SelectItem)*
                    |   "TUPLE" SelectItem
                    |   "ELEMENT" OperatorExpression
SelectItem     ::= ValueExpr [ "AS" Variable ]
                    |   WildCard
WildCard       ::= "*" # Not supported yet (ever)?
```

#### SQL++ From Clause

```
FromClause         ::= FromItem ( "," FromItem)*
FromItem           ::= FromSingle
                   |   FromJoin
                   |   FromFlatten
FromSingle         ::= FromElement "AS" Variable ["AT" OperatorExpr ] # AT not yet supported
FromJoin           ::= FromInnerJoin
                   |   FromOuterJoin
FromInnerJoin      ::= FromItem "JOIN" FromItem "ON" OperatorExpr
FromOuterJoin      ::= ( "LEFT" | "RIGHT" | "FULL" ) 
                       "JOIN" FromItem "ON" OperatorExpr
FromFlatten        ::= FromInFlatten # not supported
                   |   FromOutFlatten # not supported
FromInFlatten      ::= "FLATTEN" "("
                       OpertorExpression "AS" Variable ","
                       OpertorExpression "AS" Variable ")"
FromOutFlatten   ::=   "FLATTEN" "("
                       OpertorExpression "AS" Variable ","
                       OpertorExpression "AS" Variable ")"
FromElement        ::= DatasetExpression
                   |   ParenthesizedExpression # Currently not supported
```

#### SQL++ GROUP BY Clause

```
GroupItem        ::= OperatorExpresion [ "AS" VariableRef* ]
```

#### SQL++ ORDER BY Clause

```
OrderByItem    ::= OperatorExpression [ "ASC" | "DESC" ]
```

## SQL++ Configuration Parameters

UCSD SQL++ configuration parameters are implicitely defined in Asterix SQL++, and cannot be modified. They have been set to Asterix default behaviour.