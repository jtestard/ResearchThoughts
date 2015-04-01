# The SQL++ query language in AsterixDB


## Introduction

SQL++ is a novel query language for semi-structured data being developed at UCSD (details for the SQL++ query language can be found [here](http://forward.ucsd.edu/.html)). This document is not intended as a reference guide to the syntax and semantics SQL++ Query Language, which can already be found [here](http://arxiv.org/abs/1405.3631v3). Rather, this document intends to details the quirks and differences between the reference version of SQL++ and its implementation on AsterixDB. These differences are due to semantic differences between the "official" SQL++ and AsterixDB in terms of data model and algebra (Asterix SQL++ is constrained to the latter). Nevertheless, Asterix SQL++ is more expressive than AQL (AsterixDB's native query language), thus making AsterixDB more capable than indicated in [SQL++'s Expressiveness Benchmark](http://arxiv.org/abs/1405.3631v3). Finally, note that the SQL++ interface currently only offers query capabilities. To do any sort of data (or metadata) manipulation, the regular AQL interface must be used (a proper DML syntax will be available in the very near future).

In what follows, we detail the features of the Asterix SQL++ language in a grammar-guided manner, focusing on when they change from SQL++ : we list and briefly explain each of the productions in the 	grammar, and when Asterix SQL++ is found to be less expressive than its UCSD counterpart, we provide a suggestion of what change in AsterixDB's data model and/or algebra would allow bridging the gap.

### Statements

```
Statement           ::= ( SingleStatement ( ";" )? )* <EOF>
SingleStatement     ::= DataverseDeclaration
                    | SQLPPQuery
```
There are only two types of statements allowed in this interface, the `DataverseDeclaration` and `SQLPPQuery` statements.

### Dataverse Declaration

```
DataverseDeclaration ::= "use" "dataverse" Identifier
```

The world of data in an AsterixDB cluster is organized into data namespaces called dataverses. To set the default dataverse for a series of statements, the `use dataverse` statement is provided.

As an example, the following statement sets the default dataverse to be TinySocial.

###### Example

```
use dataverse TinySocial;
```

### SQL++ Query (SQLPPQuery)

```
SQLPPQuery          ::= ( SfwQuery | ExprQuery )
```

Asterix SQL++ is a fully composable query language. In the context of Asterix, each SQL++ expression returns zero or more Asterix Data Model (ADM) instances.

### Value Query
```
ValueQuery          ::= ( Value | Variable | NestedQuery | FunctionCall )
```

The most basic building block for any SQLPP expression is the `ValueQuery`. This can be a constant `Value` (which may be simple or complex), a reference to a query `Variable`, a `Nested Query` or a `FunctionCall`.

#### Null, Missing and Scalar Values

```
Value           ::= ( DefinedValue | MissingValue )
DefinedValue    ::= ( ComplexValueConstructor | ScalarValue | NullValue )
MissingValue    ::= "missing"
NullValue       ::= "null"
ScalarValue     ::= PrimitiveValue
PrimitiveValue  ::= ( NumberValue | StringValue | BooleanValue )
NumberValue     ::= ( <INTEGER_LITERAL> | <FLOAT_LITERAL> | <DOUBLE_LITERAL> )
StringValue     ::= <STRING_LITERAL>
BooleanValue    ::= ( "true" | "false" )
<STRING_LITERAL>    ::= ("\"" (<ESCAPE_QUOT> | ~["\""])* "\"")
                    | ("\'" (<ESCAPE_APOS> | ~["\'"])* "\'")
<ESCAPE_QUOT>       ::= "\\\""
<ESCAPE_APOS>       ::= "\\\'
<INTEGER_LITERAL>   ::= <DIGITS>
<DIGITS>            ::= ["0" - "9"]+
<FLOAT_LITERAL>     ::= <DIGITS> ( "f" | "F" )
                    | <DIGITS> ( "." <DIGITS> ( "f" | "F" ) )?
                    | "." <DIGITS> ( "f" | "F" )
DoubleLiteral       ::= <DIGITS>
                    | <DIGITS> ( "." <DIGITS> )?
                    | "." <DIGITS>
```
Constants in SQL++ can be scalar values (strings, integers, floating point values, double values or boolean constants), the `NullValue` or the `MissingValue`. SQL++ distinguishes between *missing* data and *null* data within the data model, while AQL uses the `null` keyword for both. Given the Asterix SQL++ uses the Asterix Data Model, the use of the `missing` keyword in a query will result in an error.


#### Complex Value Constructors

```
ComplexValueConstructor     ::= ( RecordConstructor | ListConstructor )
TupleValueConstructor       ::= "{" ( FieldBinding ( "," FieldBinding )* )? "}"
CollectionConstructor       ::= ( ArrayConstructor | BagConstructor )
ArrayConstructor            ::= ( ( "[" "]" ) | ( "[" ExprQuery ( "," ExprQuery )* "]" ) )
BagConstructor              ::= ( ( "{{" "}}" ) | ( "{{" ExprQuery ( "," ExprQuery )* "}}" ) )
FieldBinding                ::= StringValue ":" ExprQuery
```

SQL++ can be used to construct complex structures such as `Array`s, `Bag`s and `Tuple`s. Internally, these structures are mapped to their ADM counterparts. Namely, `Array`s are mapped to `OrderedLists`, `Bag`s are mapped to `UnorderedList`s and `Tuple`s are mapped to `Record`s.

#### Variables

```
Variable            ::= <IDENTIFIER>
<IDENTIFIER>        ::= <LETTER> (<LETTER> | <DIGIT> | <SPECIALCHARS>)*
```

A variable in SQL++ can be bound to any legal value. A variable reference refers to the value to which it is bound. A SQL++ variable binding binds the variable to its reference.

Bindings in SQL++ can either originate from the query environment (for examples from the `FromClause` of a `SfwQuery`) or from the dataverse environment (in which case the variable is bound to the contents of a dataset). If the binding of a variable cannot be found in the query environment\*, then the dataverse environment is inspected. If the binding cannot be found in the dataverse environment, then an error is thrown.

\* : internally, when this happens the variable reference is transformed into a dataset function call. 

#### Navigation Expressions
```
NavigationQuery     ::= PrimaryQuery ( NavStep )*
NavStep             ::= ( FieldNav | IndexNav )
FieldNav            ::= "." ( Identifier | StringValue )
IndexNav            ::= "[" ExprQuery "]"
```

Navigation expressions are mapped to their AQL counterparts, with the exception of the “I’m feeling lucky” style index accessor `[?]` from AQL, which Asterix SQL++ does not support. Any oddities in those operator's implementation would thus be shared with Asterix SQL++. For example, accessing non-existent fields or list elements will produce a `null` instead of a `missing`.

#### Nested Query

```
NestedQuery     ::= "(" SfwQuery ")"
```
The `NestedQuery` is behaves exactly like its UCSD SQL++ counterpart.

#### Function Calls

```
FunctionCall    ::= <IDENTIFIER> "(" ( ExprQuery ( "," ExprQuery )* )? ")"
```

Function calls behave like their UCSD SQL++ counterparts. Only Asterix builtin functions are available. 

### Arithmetic and Logical Expressions

```
ExprQuery           ::= AndQuery ( "or" AndQuery )?
AndQuery            ::= RelationshipQuery ( "and" RelationshipQuery )?
RelationshipQuery   ::= AddQuery ( ( "<" | ">" | "<=" | 
                         ">=" | "=" | "!=" | "~=" ) AddQuery )?
AddQuery            ::= MultQuery ( ( "+" | "-" ) MultQuery )*
MultExpression      ::= UnaryQuery ( ( "*" | "/" | "%" |
                         "^"| "idiv" ) UnaryQuery )*
UnaryQuery          ::= ( ( "+" | "-" ) )? NavigationQuery
```

Arithmetic and Logical operators are mapped to their AQL counterparts.

### Select-From-Where Query (SfwQuery)

```
SfwQuery            ::= ( SfwQuerySelectFirst | SfwQuerySelectLast )
SfwQuerySelectFirst ::= SelectClause FromClause ( WhereClause )? ( GroupByClause )? (OrderByClause)? (LimitClause)?
SfwQuerySelectLast  ::= FromClause ( WhereClause )? ( GroupByClause )? (OrderByClause)? (LimitClause)? SelectClause
```

The `SfwQuery` expression has all the clauses of the reference implementation, but their individual behaviors differ, as we will see next.

### Select Clause

```
SelectClause            ::= "select" ("distinct")? (
                              SelectElementClause
                            | SelectAttributeClause
                            | SelectTupleClause
                        )
SelectTupleClause       ::= ( ( ExprQuery ( "as" Alias )? ) ( ( "," ExprQuery ( "as" Alias )? ) )* )
Alias                   ::= StringValue
```

Asterix SQL++ supports the `Select Element` clause (which is equivalent to the AQL `Return` clause) and the syntactic sugar `Select Tuple` clause but not the `Select Attribute` clause. The latter isn't supported simply because Asterix does not have an operator which allows iterating over field bindings of a tuple. Finally, the `Distinct` keyword is not supported because AsterixDB doesn't know how to do deep complex equality.


### From Clause 

##### Single Element

```
FromClause  ::= "from" FromItem
FromItem    ::= ( FromSingleItem | FromBinaryItem | FromFlattenItem )
FromSingleItem      ::= ( FromCollectionItem | FromTupleItem )
FromCollectionItem  ::= ExprQuery "as" elementVar ( "at" positionVar )?
FromTupleItem       ::= ExprQuery "as" "{" fieldNameVar ":" fieldValueVar "}"
elementVar          ::= Variable
positionVar         ::= Variable
fieldNameVar        ::= Variable
fieldValueVar       ::= Variable
```

Asterix SQL++ supports ranging over collection elements, but not ranging over tuple attributes. Again, the latter isn't supported simply because Asterix does not have an operator which allows iterating over field bindings of a tuple.

##### Joins

The examples we have seen so far pulled their data from a single datasource. Like in SQL, SQL++ allows the join of multiple data sources.

```
FromBinaryItem          ::= ( FromCorrelateItem
                            | FromJoin
                            | FromCartesianProduct
                            )
FromCartesianProduct    ::= FromLeft "," FromRight
FromJoin                ::= ( FromInnerJoin
                            | FromLeftOuterJoin
                            | FromFullOuterJoin
                            )
FromInnerJoin           ::= FromLeft ( "inner" )? "join" FromRight ( "on" ExprQuery )?
FromLeftOuterJoin       ::= FromLeft "left" ( "outer" )? "join" FromRight ( "on" ExprQuery )?
FromFullOuterJoin       ::= FromLeft "full" ( "outer" )? "join" FromRight "on" ExprQuery
FromLeft                ::= FromSingleItem
FromRight               ::= FromItem

FromFlattenItem         ::= ( FromInnerFlatten | FromOuterFlatten )
FromInnerFlatten        ::= "inner" "flatten" "(" OuterExprQuery "as" outerVar "," InnerExprQuery "as" innerVar ")"
FromOuterFlatten        ::= "outer" "flatten" "(" OuterExprQuery "as" outerVar "," InnerExprQuery "as" innerVar ")"
outerVar                ::= Variable
innerVar                ::= Variable
OuterExprQuery          ::= ExprQuery
InnerExprQuery          ::= ExprQuery

FromCorrelateItem       ::= ( FromInnerCorrelateItem
                            | FromLeftCorrelateItem
                            | FromFullCorrelateItem
                            )
FromInnerCorrelateItem  ::= FromLeft "inner" "correlate" FromRight
FromLeftCorrelateItem   ::= FromLeft "left" ( "outer" )? "correlate" FromRight
FromFullCorrelateItem   ::= FromLeft "full" ( "outer" )? "correlate" FromRight "on" ExprQuery
```

Asterix SQL++ supports fully the reference implementation of the `inner correlate` clause as well as the syntactic sugar expressions `inner flatten` and `inner join`.

Asterix SQL++ supports partially the `left correlate` expression. To understand exactly what is supported, we look at the Asterix algebra. The operation which is supported is the `left-outer-join` operation, which only handles data that is structurally uncorrelated. Any use of the `left correlate` on data which is structurally correlated is not supported. In order to support such use cases, an `outer-unnest` physical implementation in the AsterixDB query execution engine would be necessary.

Here are two examples of queries using `left correlate`, the former is supported while the latter is not :

Left Correlate on Structurally Uncorrelated Data

```
select user.name as name, message.content as message
from FacebookUsers as user
left correlate FacebookMessages as message
where user.id = message.author-id;
```

Left Correlate on Structurally Correlated Data

```
select user.name as name, employment.start-date as start-date
from FacebookUsers as user
left correlate user.employments as employment;
```

The direct consequence of this is that the `outer flatten` expression is not supported.

The restrictions apply furthermore when subqueries are involved. The `left-correlate` expressions with a nested query argument is supported if the following conditions are met :

 1. The arguments of the nested from clause are not structurally correlated to the left item of the `left-correlate` (which would be the `FacebookUsers as user` expression in the example below).
 2. No other clause besides the `select`, `from` and `where` exists in the nested query.

Here is an example of a query which is supported in Asterix SQL++

```
select user.name as name, message.content as message
from FacebookUsers as user
left correlate (
    select element message
    from FacebookMessages as message
	where user.id = message.author-id
) as message;
```

The second restriction mentionned above is not a consequence of the absence of `outer-unnest`, rather it is due to the difficulty of the query rewriting of such use cases in the absence of the `missing` keyword in the data model.

### Where Clause

```
WhereClause ::= "where" ExprQuery
```
The `WhereClause` behaves exactly as its UCSD SQL++ counterpart.

### Group By

```
GroupByClause   ::= "group by" GroupByItem ( "," GroupByItem )*
GroupByItem     ::= ExprQuery "as" GroupingVariable
GroupingVariable::= Variable
```

The `GroupBy` clause in AsterixDB is very close to the reference implementation and provides the special `group` variable. However, there are a number of differences :

 - It requires incoming values to be homogeneous (all records, all lists, all strings ...).
 - It also requires grouping attributes to be homogeneous, because the Asterix equality operation cannot compare values with different data types.

### Order By Clause and 

```
OrderByClause   ::= "order by" OrderByItem ( "," OrderByItem)* (LimitClause)? (OffsetClause)?
OrderByItem     ::= ExprQuery ( "asc" | "desc" )
```

The `OrderBy` behaves exactly the same as AQL in the [SQL++'s Expressiveness Benchmark](http://arxiv.org/abs/1405.3631v3).

### Limit Clause

```
LimitClause     ::= "limit" ExprQuery
OffsetClause    ::= "offset" ExprQuery
```

These clauses are behave exactly like the reference implementation.