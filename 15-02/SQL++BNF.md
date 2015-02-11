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


