# The SQL++ query language for Asterix, Version Alpha

## Introduction

This document is intended as a reference guide to the full syntax and semantics of the SQL++ Query Language for Asterix (Asterix SQL++). This document describes how you should write SQL++ queries in the context of AsterixDB. Details for the SQL++ query language being developed at UCSD can be found [here](http://forward.ucsd.edu/.html). Note that *you do not need to know AQL to use SQL++*, a prior knowledge of SQL is sufficient. However, it is important to note that while we are using the SQL++ query language, we are keeping the Asterix Data Model (ADM). As such, readers are advised to read and understand the [ADM reference guide](/aql/datamodel.html) since a basic understanding of ADM concepts is a prerequisite to understanding SQL++.

For those already aware of SQL++ prior to its use in the context of AsterixDB, note that there will be some differences between the language presented here and the [SQL++ developed at UCSD](http://arxiv.org/abs/1405.3631v3). In particular, the Asterix version of SQL++ does not contain *configurations*. Instead, the configurations are implicitly defined as being those of Asterix according to the [SQL++ Expressiveness Benchmark](http://arxiv.org/abs/1405.3631v3). Finally, note that the SQL++ interface currently only offers query capabilities. To do any sort of data (or metadata) manipulation, the regular AQL interface must be used (a proper DML syntax will be available in the very near future).

In what follows, we detail the features of the SQL++ language in a grammar-guided manner: We list and briefly explain each of the productions in the SQL++ grammar, offering examples for clarity in cases where doing so seems needed or helpful.

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

The world of data in an AsterixDB cluster is organized into data namespaces called dataverses. To set the default dataverse for a series of statements, the use dataverse statement is provided.

As an example, the following statement sets the default dataverse to be TinySocial.

###### Example

```
use dataverse TinySocial;
```

### SQL++ Query (SQLPPQuery)

```
SQLPPQuery          ::= ( SfwQuery | ExprQuery )
```

SQL++ is a fully composable query language. In the context of Asterix, each SQL++ expression returns zero or more Asterix Data Model (ADM) instances. There are two major kinds of query expressions in AQL. At the topmost level, an SQL++ query expression can be an `ExprQuery` (similar to a mathematical expression) or a `SfwQuery` (similar to the SQL Select-From-Where query expression). Each will be detailed as we explore the full SQL++ grammar.

### Value Query
```
ValueQuery          ::= ( Value | Variable | NestedQuery | FunctionCall )
```

The most basic building block for any SQLPP expression is the ValueQuery. This can be a constant `Value` (which may be simple or complex), a reference to a query `Variable`, a `Nested Query` or a function call.

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

The following are some simple examples of SQL++ constants. Since SQL++ is an expression language, each example is also a complete, legal SQL++ query (!).

###### Examples 

```
"a string"
42
null
missing -- will result in error   
```

#### Complex Value Constructors

```
ComplexValueConstructor     ::= ( RecordConstructor | ListConstructor )
RecordConstructor           ::= ( ( "[" "]" ) | ( "[" ( Identifier | StringValue ) ":" ExprQuery ( "," ( Identifier | StringValue ) ":" ExprQuery )* "]" ) )
ListConstructor             ::= ( OrderedListConstructor | UnorderedListConstructor )
OrderedListConstructor      ::= ( ( "[" "]" ) | ( "[" ExprQuery ( "," ExprQuery )* "]" ) )
UnorderedListConstructor    ::= ( ( "{{" "}}" ) | ( "{{" ExprQuery ( "," ExprQuery )* "}}" ) )
```

SQL++ can be used to construct complex  structures inherited from the ADM. This is accomplished using constructors for each of the major ADM complex object structures, namely lists (ordered or unordered) and records. Ordered lists are like JSON arrays, while unordered lists have bag (multiset) semantics. Records are built from attributes that are field-name/field-value pairs, again like JSON. (See the AsterixDB Data Model document for more details on each.)

The following examples illustrate how to construct a new ordered list with 3 items, a new unordered list with 4 items, and a new record with 2 fields, respectively. List elements can be homogeneous (as in the first example), which is the common case, or they may be heterogeneous (as in the second example). The data values and field name values used to construct lists and records in constructors are all simply SQL++ expressions. Thus the list elements, field names, and field values used in constructors can be simple literals (as in these three examples) or they can come from query variable references or even arbitrarily complex SQL++ expressions.

###### Examples

```
[ "a", "b", "c" ]

{{ 42, "forty-two", "AsterixDB!", 3.14f }}

{
  "project name": "AsterixDB"
  "project members": {{ "vinayakb", "dtabass", "chenli" }}
}
```

###### Note

When constructing nested records there needs to be a space between the closing braces to avoid confusion with the }} token that ends an unordered list constructor: `{ "a" : { "b" : "c" }}` will fail to parse while `{ "a" : { "b" : "c" } }` will work.

#### Variables

```
Variable            ::= <IDENTIFIER>
<IDENTIFIER>        ::= <LETTER> (<LETTER> | <DIGIT> | <SPECIALCHARS>)*
```

A variable in SQL++ can be bound to any legal ADM value. A variable reference refers to the value to which it is bound. A SQL++ variable binding binds the variable to its reference.

Bindings in SQL++ can either originate from the query environment (for examples from the `FromClause` of a `SfwQuery`) or from the dataverse environment (in which case the variable is bound to the contents of a dataset). If the binding of a variable cannot be found in the query environment, then the dataverse environment is inspected. If the binding cannot be found in the dataverse environment, then an error is thrown.        

###### Examples

```
select fb as user
from FacebookUsers as fb
```

In this query, the `FacebookUsers` variable is bound to the FacebookUsers dataset of the TinySocial dataverse and the `fb` variable is bound incrementally to each record from the `FacebookUsers` dataset.

#### Navigation Expressions
```
NavigationQuery     ::= PrimaryQuery ( NavStep )*
NavStep             ::= ( FieldNav | IndexNav )
FieldNav            ::= "." ( Identifier | StringValue )
IndexNav            ::= "[" ExprQuery "]"
```

Components of complex types in ADM are accessed via `NavigationQuery`s (or path accesses). Navigation expressions can be applied to the result of an SQL++ expression that yields an instance of such a type, e.g., a record or list instance. This expression will typically be a `Variable` but can also be a `ComplexValueConstructor` or a `NestedQuery`. 

For records, path access is based on field names. If the field name contain a `-` symbol, quotes must be used around the identifier. For ordered lists, path access is based on (zero-based) array-style indexing. SQL++ does not support the “I’m feeling lucky” style index accessor `[?]` from AQL. The Asterix version of SQL++ differs from its UCSD counterpart in that accessing non-existent fields or list elements will produce a `null` instead of a `missing`.

The following examples illustrate field access for a record, index-based element access for an ordered list, and also a composition thereof.

###### Examples

```
({"list": [ "a", "b", "c"]}).list

({"mickey-mouse" : "mouse", "snoopy" : "dog"})."mickey-mouse"

(["a", "b", "c"])[2]

({ "list": [ "a", "b", "c"]}).list[2]
```

#### Nested Query

```
NestedQuery     ::= "(" SfwQuery ")"
```
The `NestedQuery` is very similar to its SQL counterpart.

#### Function Calss

```
FunctionCall    ::= <IDENTIFIER> "(" ( ExprQuery ( "," ExprQuery )* )? ")"
```

Function calls cannot be used as of yet. They will be introduced to the SQL++ language shortly.

<!--
Functions are included in SQL++, like most languages, as a way to package useful functionality or to componentize complicated or reusable SQL++ computations. A function call is a legal SQL++ query expression that represents the ADM value resulting from the evaluation of its body expression with the given parameter bindings; the parameter value bindings can themselves be any SQL++ expressions. 

The following example is a (built-in) function call expression whose value is 8.

```
string-length("a string")
```
-->

### Expression Query (ExprQuery)

#### Logical Expressions

```
ExprQuery           ::= AndQuery ( "or" AndQuery )?
AndQuery            ::= RelationshipQuery ( "and" RelationshipQuery )?
```

As in most languages, boolean expressions can be built up from smaller expressions by combining them with the logical connectives and/or. Legal boolean values in SQL++ are `true`, `false`, and `null`. (Nulls in SQL++ are treated much like SQL treats its unknown truth value in boolean expressions.)

###### Example

The following is an example of a conjunctive range predicate in SQL. It will yield `true` if `a` is bound to `4`, `null` if `a` is bound to `null`, and `false` otherwise.

```
a > 3 and a < 5
```

#### Comparison Expressions

```
RelationshipQuery   ::= AddQuery ( ( "<" | ">" | "<=" | 
                         ">=" | "=" | "!=" | "~=" ) AddQuery )?
```

SQL++ has all the usual operators for comparing pairs of atomic values. It also has an extra operator, which is the “roughly equal” operator provided for similarity queries. Similarity queries are not yet supported in SQL++ (only AQL), but will in some near future.

An example comparison expression (which yields the boolean value true) is shown below.

###### Example

```
5 > 3
```  

#### Arithmetic Expressions

```
AddQuery            ::= MultQuery ( ( "+" | "-" ) MultQuery )*
MultExpression      ::= UnaryQuery ( ( "*" | "/" | "%" |
                         "^"| "idiv" ) UnaryQuery )*
UnaryQuery          ::= ( ( "+" | "-" ) )? NavigationQuery
```

AQL also supports the usual cast of characters for arithmetic expressions. The example below evaluates to 25.

###### Example

```
3 ^ 2 + 4 * 4
```

### Select-From-Where Query (SfwQuery)

```
SfwQuery            ::= ( SfwQuerySelectFirst | SfwQuerySelectLast )
SfwQuerySelectFirst ::= SelectClause FromClause ( WhereClause )? ( GroupByClause )? (OrderByClause)?
SfwQuerySelectLast  ::= FromClause ( WhereClause )? ( GroupByClause )? (OrderByClause)? SelectClause

SelectClause            ::= "select" ("distinct")? (
                              SelectElementClause
                            | SelectAttributeClause
                            | SelectTupleClause
                        )
SelectTupleClause       ::= ( ( ExprQuery ( "as" Alias )? ) ( ( "," ExprQuery ( "as" Alias )? ) )* ) 
Alias                   ::= StringValue

FromClause  ::= "from" FromItem
FromItem    ::= ( FromSingleItem | FromBinaryItem | FromFlattenItem )
FromSingleItem      ::= ( FromCollectionItem | FromTupleItem )
FromCollectionItem  ::= ExprQuery "as" elementVar ( "at" positionVar )?
FromTupleItem       ::= ExprQuery "as" "{" fieldNameVar ":" fieldValueVar "}"
elementVar          ::= Variable
positionVar         ::= Variable
fieldNameVar        ::= Variable
fieldValueVar       ::= Variable

WhereClause ::= "where" ExprQuery
```

A `SfwQuery` is the standard way to query the AsterixDB database using SQL++. Each `SfwQuery` retrieves zero or more values from the database. However, it differs from its SQL counterpart in that the `SelectClause` can be located at the beginning of a query (more SQL-like) or at the end (more AQL-like).
 
A `FromClause` may contain a single `FromItem`. The `FromItem` itself may be a `FromSingleItem` possibly followed by a `FromCorrelateItem`, or a `FromFlattenItem`. The `FromClause` is used to establish variable bindings in the `SfwQuery`. 

The `FromSingleItem` may be a `FromCollectionItem` or a `FromTupleItem`. The `FromCollectionItem` is what most closely resembles the AQL `For` clause. Like the AQL `ForClause`, it binds a variable (the `elementVar`) incrementally to each element of the result of the evaluation of the `ExprQuery`, and includes an optional positional variable (the `positionVar`). The output of this clause would be a collection of tuples of variable bindings (which we will call "binding tuples").

The `FromTupleItem` assumes that the result of the evaluation of the `ExprQuery` is an ADM `Record`. It then ranges over field bindings for that record and binds the field name and the field value of that binding to the `fieldNameVar` and `fieldValueVar`. This clause is especially useful if your datasets have records with a large number of field bindings on which you wish to iterate. For the moment, the `FromTupleItem` isn't implemented in Asterix. Therefore, its use in a query in the Asterix context will result in an error.

The `WhereClause` does the same thing as its AQL and SQL counterparts. It takes as input a collection of binding tuples and filters it according to some condition.

The `SelectTupleClause` is the equivalent to the SQL `SELECT` clause. It takes as input a collection of binding tuples, evaluates its `ExprQuery`s according to that input collection, then creates a record in which each field name is an `Alias` and each field value is the result of the corresponding `ExprQuery` evaluation. Note that while aliases are not required, in the absence of alias one will be generated for the given `ExprQuery`.

The first example shows a `SfwQuery` that selects a single record from the dataset FacebookUsers using a `FromCollectionItem`. The second examples iterates over an ordered list, retaining the position of each item.

###### Example 1

```
select user as user 
from FacebookUsers as user
where user.id = 8;
```

###### Example 2

```
select val as value, p as position
from [ "SQL++" , "is", "awesome" ] as val at p 
```

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
```

The `FromBinaryItem` is what allows SQL++ to query from multiple data sources. The `FromBinaryItem` can be a `FromCorrelateItem`, a `FromJoin` or a `FromCartesianProduct`. The `FromCartesianProduct` has a similar behavior to its ANSI SQL counterpart.

A `FromJoin` can be a `FromInnerJoin`, a `FromLeftOuterJoin` or a `FromFullOuterJoin`. Again, those items are similar to their SQL counterparts. Note that the `FromLeftOuterJoin` and `FromFullOuterJoin` are not yet supported.

The next example shows a `SfwQuery` that joins two datasets, FacebookUsers and FacebookMessages, returning user/message pairs. The results contain one record per pair, with result records containing the user’s name and an entire message. The example is shown under two forms should be familiar to SQL users.

###### Cartesian Product Example
```
from FacebookUsers as user, FacebookMessages as message
where user.id = message."author-id"
select user.name as uname, message.message as message
```

###### Inner Join Example

```
from FacebookUsers as user
join FacebookMessagesa as messages
on user.id = message."author-id"
select user.name as uname, message.message as message
```

The `FromFlattenItem` is used to unnest nested collections.

```
FromFlattenItem     ::= ( FromInnerFlatten | FromOuterFlatten )
FromInnerFlatten    ::= "inner" "flatten" "(" OuterExprQuery "as" outerVar "," InnerExprQuery "as" innerVar ")"
FromOuterFlatten    ::= "outer" "flatten" "(" OuterExprQuery "as" outerVar "," InnerExprQuery "as" innerVar ")"
outerVar            ::= Variable
innerVar            ::= Variable
OuterExprQuery      ::= ExprQuery
InnerExprQuery      ::= ExprQuery
```

The `outerVar`/`innerVar` are bound to the result of the evaluation of the `OuterExprQuery`/`innerExprQuery` respectively. The `InnerExprQuery` is typically correlated to the `outerVar` (for example, the `InnerExprQuery` could be a path navigation such as `outerVar.attrName` where `outerVar.attrName` evaluates to an ADM list). At the moment, only the `InnerFlatten` is available.

The following query will produce a record for each employment of each Facebook user.

###### Inner Flatten Example

```
select fb.name as name, emp as employment
from inner flatten (
  FacebookUsers as fb,
  fb.employment as emp
);
```

The `FromCorrelateItem`s are the building blocks used to join data in SQL++.                             

```
FromCorrelateItem       ::= ( FromInnerCorrelateItem
                            | FromLeftCorrelateItem
                            | FromFullCorrelateItem
                            )
FromInnerCorrelateItem  ::= FromLeft "inner" "correlate" FromRight
FromLeftCorrelateItem   ::= FromLeft "left" ( "outer" )? "correlate" FromRight
FromFullCorrelateItem   ::= FromLeft "full" ( "outer" )? "correlate" FromRight "on" ExprQuery
```

The `FromCorrelate` can translate into a `FromInnerCorrelate`, a `FromLeftOuterCorrelate` or a `FromFullOuterCorrelate`. 

For each binding tuple obtained by evaluating the `FromLeft` expression, the `FromRight` bindings are evaluated and for each such tuple the `FromLeftCorrelate` and `FromInnerCorrelate` expressions output the concatenation of the bindings obtained from `FromLeft` and `FromRight`.
In the case where no bindings are found when evaluating `FromRight`, the `FromInnerCorrelate` outputs nothing while `FromLeftCorrelate` outputs a single binding tuple in which each variable from the `FromRight` clause is bound to null.

Some examples a provided along with their output prepended by a `>>`.

```
from [
    {"id" : 1},
    {"id" : 2, "outer" : [{"inner" : 1}, {"inner" : 2}]}
] as left
inner correlate left.outer as right
select left.id as id, right.inner as inner;

>> {"id" : 2, "inner" : 1 }
>> {"id" : 2, "inner" : 2 }

from [
    {"id" : 1},
    {"id" : 2, "outer" : [{"inner" : 1}, {"inner" : 2}]}
] as left
left correlate left.outer as right
select left.id as id, right.inner as inner;

>> {"id" : 1, null }
>> {"id" : 2, "inner" : 1 }
>> {"id" : 2, "inner" : 2 }
```

Notice that both `FromInnerCorrelate` and `FromLeftCorrelate` behave like a SQL cartesian product if the left and right items are not correlated.

```
// You can replace "inner" by "left" and get the same output
from [
    {"id" : 1, "name" : "alice"},
    {"id" : 2, "name" : "bob"}
] as left 
from inner correlate [
    {"id" : 1, "age" : 18},
    {"id" : 2, "age" : 31}
] as right
select left as left, right as right 

>> {"left" : {"id" : 1, "name" : "alice" }, "right" : {"id" : 1, "age" : 18} }
>> {"left" : {"id" : 1, "name" : "alice" }, "right" : {"id" : 2, "age" : 31} }
>> {"left" : {"id" : 2, "name" : "bob" }, "right" : {"id" : 1, "age" : 18} }
>> {"left" : {"id" : 2, "name" : "bob" }, "right" : {"id" : 2, "age" : 31} }
```

The `FromFullCorrelate` returns the output of the `FromLeftCorrelate` filtered according to some condition. In addition, for each binding tuple from the `FromRightCorrelate` which has no match in the `FromLeft` according to the condition, it outputs a single binding tuple in which each variable from the `FromLeft` clause is bound to null. The `FromFullCorrelate` is currently unavailable in Asterix but may be implemented in the future.

Finally, note that the `FromJoin`, `FromFlattenItem` and `FromCartesianProduct` we have seen before do not add any "expressive power" to the SQL++ language, i.e. you could simulate them with `FromCorrelateItem` and other SQL++ expressions.

Here are some of the previous queries we saw rewritten using `InnerCorrelate`.

###### Examples

```
from FacebookUsers as user
inner correlate FacebookMessages as message
where user.id = message."author-id"
select user.name as uname, message.message as message

select fb.name as name, emp as employment
from FacebookUsers as fb
inner correlate fb.employment as emp;
```

The `SelectElementClause`s and `SelectAttributeClause`s are the building blocks used to return data in SQL++. 

```
SelectElementClause     ::= <ELEMENT> ExprQuery
SelectAttributeClause   ::= <ATTRIBUTE> NameExpr <COLON> ValExpr
NameExpr                ::= ExprQuery
ValExpr                 ::= ExprQuery
``` 

The `Select Element` clause is the equivalent of the `AQL` return clause. It allows return any type of `ExprQuery`. Typically, that `ExprQuery` will be a `ComplexValueConstructor` or a `Variable`, as shown in this example.

###### Select Element Example 
```
select element { "id" : user.id. "user" : user }
from FacebookUsers as user
```

The `SelectAttribute` clause allows to output a single record where the field-name/field-value pairs are determined by the input bindings. For each input binding tuple, the result of the evaluation of the `NameExpr` and `ValExpr` are added into a new field-name/field-value pair into the same record. The `SelectAttribute` clause is not supported by Asterix.

Below this line work is still in progress. 

--------------------------

### Group By and Order By Clause

```
GroupByClause   ::= "group by" GroupByItem ( "," GroupByItem )*
GroupByItem     ::= ExprQuery "as" GroupingVariable
GroupingVariable::= Variable

OrderByClause   ::= "order by" OrderByItem ( "," OrderByItem)* (LimitClause)? (OffsetClause)?
OrderByItem     ::= ExprQuery ( "asc" | "desc" )
LimitClause     ::= "limit" ExprQuery
OffsetClause    ::= "offset" ExprQuery
```

The `GroupBy` clause is used in SQL++ for aggregation, much like the `GROUP BY` of SQL. However, its semantics differ and are explained through an example. First, it requires incoming values to be homogeneous (all records, all lists, all strings ...). Then it groups all values according to some `GroupByItem`s ( `person.employer as employer` in this example). Finally it outputs a binding tuple with a binding variable for each grouping which is bound to the value of the `GroupingVariable` (`"McDonalds"` , `"unknown"` or `null` in our example). The binding tuple also contains an additional variable called `group` which contains the unordered list of the values that were grouped together.

```
from {{
    {"id" : 1, "name" : "alice", "employer" : "McDonald's" },
    {"id" : 2, "name" : "bob", "employer" : "unknown" },
    {"id" : 3, "name" : "chad", "employer" : null },
    {"id" : 4, "name" : "david" },
    {"id" : 5, "name" : "esther", "employer" : "McDonald's" }
}} as person
group by person.employer as employer
select employer as employer, group as group

>> { "employer" : "McDonald's" , group : {{
>>    {"id" : 1, "name" : "alice", "employer" : "McDonald's" },
>>    {"id" : 5, "name" : "esther", "employer" : "McDonald's" }
>> }} }
>> { "employer" : "unknown", group : {{ {"id" : 2, "name" : "bob", "employer" : "unknown" } }} }
>> { "employer" : null, group : {{
>>    {"id" : 3, "name" : "chad", "employer" : null },
>>    {"id" : 4, "name" : "david" } 
>> }} }
```

The `GroupByClause` and `OrderByClause` are not yet available, but will be so shortly.