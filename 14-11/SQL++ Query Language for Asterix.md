# The SQL++ query language for Asterix


## Introduction

This document is intended as a reference guide to the full syntax and semantics of the SQL++ Query Language for Asterix (Asterix SQL++). This document describes how the SQL++ query language is interpreted in the context of AsterixDB. Details for the SQL++ query language being developped at UCSD can be found [here](http://forward.ucsd.edu/sqlpp.html).

It is important to note that while we are using the SQL++ query language, we are keeping the Asterix Data Model. As such, there will be some differences between the language presented here and the standard "UCSD" SQL++ [1]. These differences will be clearly highlighted when they occur and will be kept at a minimum.

This description only addresses expressions for the moment. Unsupported expressions are currently greyed out.

## Expressions
```python
	SQLPPQuery ::= SQLPPExpression
```	
A SQL++ query can be any legal SQL++ expression.

```python
	SQLPPExpression ::= 	SFWExpression
			|		SQLPPOperatorExpr
			|		SQLPPQuantifiedExpression
```

The `SQLPPQuantifiedExpression` expression specification will be deferred to a later date, given that existential/universal quantification is not fully supported in tbe SQL++ implementation as of this moment (in particular the `IN, EXISTS, ANY, ALL` keywords from the SQL++ language are currently not supported).

### SQL++ Operator Expression

```python
	SQLPPOperatorExpr 	::= SQLPPAndExpr ( "or" AndExpr )*
	SQLPPAndExpr      	::= SQLPPRelExpr ( "and" RelExpr )*
	SQLPPRelExpr 		::= SQLPPAddExpr ( ( "<" | ">" | "<=" | 
						">=" | "=" | "!=" | "~=" ) AddExpr )?
	SQLPPAddExpr  		::= SQLPPMultExpr ( ( "+" | "-" ) SQLPPMultExpr )*
	SQLPPMultExpr 		::= SQLPPUnaryExpr ( ( "*" | "/" | "%" 
						| "^"| "idiv" ) SQLPPUnaryExpr )*
	SQLPPUnaryExpr 		::= ( ( "+" | "-" ) )? SQLPPValueExpr
```

The operator expression structure is inherited from AQL.

#### SQL++ Value Expression

```python
	SQLPPValueExpr ::= 	SQLPPValue
			|	SQLPPParenthesizedExpression
			|	SQLPPVariableRef
			|	SQLPPPathStep
			|	SQLPPNamedValue
			|	SQLPPFunctionCallExpr
```
					
#### SQL++ Value

```python
	SQLPPValue 			::= SQLPPDefinedValue
				|	"missing"
	SQLPPDefinedValue	::= SQLPPScalarValue
				|	SQLPPComplexValue
	SQLPPComplexValue	::= SQLPPTupleValue
				|	SQLPPBagValue
				|	SQLPPArrayValue
				|	SQLPPMapValue
	SQLPPScalarValue	::= SQLPPPrimitveValue
				|	SQLPPEnrichedValue
	SQLPPPrimitveValue	::= StringLiteral*
				|	SQLPPNumberValue
				|	"true"
				|	"false"
				|	"null"
	SQLPPNumberValue	::= IntegerLiteral*
				|	FloatLiteral*
				|	DoubleLiteral*
	SQLPPEnrichedValue	::= TypeName "(" SQLPPPrimitiveValue 
							( "," SQLPPPrimitiveValue ) ? ")"
	SQLPPTupleValue		::= RecordConstructor*
	SQLPPBagValue		::= UnorderedListConstructor*
	SQLPPArrayValue		::= OrderedListConstructor*
	SQLPPMapValue		::= "map" "(" SQLPPValue ":" SQLPPDefinedValue 
							( "," SQLPPValue ":" SQLPPDefinedValue ) ")"
```
	
This section is inspired by the SQL++ Value BNF presented in [1]. However, some features from the BNF are not included. For example,
the `id::` field for defined values is absent from this specification. In order to map more closely to AQL primitives, the number value is subdivided further to its AQL equivalents. Primitive values imported from AQL are appended with a `*`.

#### SQL++ Parenthesized Expression

```python
	SQLPPParenthesizedExpression ::= "(" SFWExpression ")"
```
	
#### SQL++ Variable Ref

```python
	SQLPPVariableRef 	::= VariableRef*
```
	
#### SQL++ PathStep

```python
	SQLPPPathstep 	::= SQLPPOperatorExpr "." Identifier*
			|	SQLPPOperatorExpr "[" SQLPPValueExpr "]"
			|	SQLPPOperatorExpr "->" SQLPPValueExpr
```

Notice that SQL++ does not have the "I am lucky" array navigation AQL has (the "?" in array navigation).			
#### SQL++ Named Value

```python
	SQLPPNamedValue ::= QualifiedName*
```

#### SQL++ Function Call Expression

```python
	SQLPPFunctionCallExpr 	::= "(" SQLPPExpression ( "," SQLPPExpression ) ? ")"
```

In AQL, the symbols `"<" | ">" | "<=" | ">=" | "=" | "!=" | "~=" | "+" | "-" | "*" | "%" | "/" ` are treated as special operators while in SQL++ they are treated as functions. We chose to keep the AQL format.

### SQL++ SFWExpression

	SQLPPSFWExpression ::=	"SELECT"  ["DISTINCT"] SQLPPSelectClause
				|	"FROM" SQLPPFromItem
				|	"WHERE" SQLPPOperatorExpr
	#					|	"GROUPBY" SQLPPGroupItem
	#					|	"HAVING" SQLPPOperatorExpr
	#					|	("UNION" | "INTERSECT" | "EXCEPT") ["ALL"] SQLPPSFWExpression
	#					|	"ORDER BY" SQLPPOrderItem
	#					|	"LIMIT" SQLPPOperatorExpr
	#					|	"OFFSET" SQLPPOperatorExpr


#### SQL++ Select Clause

```python
	SQLPPSelectClause	::= ["TUPLE"] SQLPPSelectItem
	#					|	"ELEMENT" SQLPPOperatorExpr
	SQLPPSelectItem		::= SQLPPOperatorExpr [ "AS" Identifier* ]
```

#### SQL++ From Clause

```python
	SQLPPFromItem	::= SQLPPFromSingle
				|	SQLPPFromJoin
				|	SQLPPFromFlatten
	SQLPPFromSingle		::=	SQLPPOperatorExpr "AS" VariableRef* ["AT" SQLPPOperatorExpr ]
	SQLPPFromJoin		::=	SQLPPFromInnerJoin
	#					|	SQLPPFromOuterJoin
	SQLPPFromInnerJoin	::= "JOIN" SQLPPFromItem "ON" SQLPPOperatorExpr
	# SQLPPFromOuterJoin	::= ( "LEFT" | "RIGHT" | "FULL" ) 
	#					"JOIN" SQLPPFromItem "ON" SQLPPOperatorExpr
	# SQLPPFromFlatten	::= SQLPPFromInFlatten
	#					| SQLPPFromOutFlatten
	# SQLPPFromInFlatten ::= "FLATTEN" "("
	#					SQLPPOpertorExpr "AS" VariableRef* ","
	#					SQLPPOpertorExpr "AS" VariableRef* ")"
	# SQLPPFromOutFlatten::= "FLATTEN" "("
	#					SQLPPOpertorExpr "AS" VariableRef* ","
	#					SQLPPOpertorExpr "AS" VariableRef* ")"
```

#### SQL++ GROUP BY Clause

```python
	# SQLPPGroupItem		::= SQLPPOperatorExpr [ "AS" VariableRef* ]
```

#### SQL++ ORDER BY Clause

```python
	# SQLPPOrderByItem	::= SQLPPOperatorExpr [ "ASC" | "DESC" ]
```

## SQL++ Configuration Parameters

UCSD SQL++ configuration parameters are implicitely defined in Asterix SQL++, and cannot be modified. They have been set to Asterix default behaviour.

## Notes

#### SQL++ Type Names

SQL++ does not provide a mechanism to identify a type, while AQL does. It seems like this would be a useful feature for an implementation of the SQL++ language.

We propose to introduce a type naming. The same way there can be a *named value*, we introduce the concept of a *named type*. We can evaluate later if such addition makes sense outside of the AQL context later.

#### SQL++ Named Values

Given SQL++ *named values*

#### SQL++ Select Clause

Note sure whether `SQLPPSelectItem	::= SQLPPOperatorExpr [ "AS" {{Identifier}}* ]` is correct. Other candidates include `VariableRef`, `QualifiedName` and more.
