## AQL - SQLPP Type Mappings

These mapping have to do with how queries are constructed only. Internal types in Asterix are consistent with the capabilities of the Asterix operators.

The work consists of removing the Value package from the `asterix-sqlpp` module and replace it with AQL types. This is expected to create changes :

 - In the SQL++ visitor classes
 - In the Ast2Plan translator

#### Literal Types

*SQL++ Type => AQL Type*

 - StringValue => StringLiteral
 - NullValue => NullLiteral
 - BooleanValue => TrueLiteral / FalseLiteral
 - NumberValue => Integer/LongInteger/Float/Double Literal

#### Complex Types

*SQL++ Type => AQL Type*

- ArrayValue => ListConstructor (type ordered)
- BagValue => ListConstructor (type unordered)
- TupleValue => RecordConstructor

Strategy :

 1. Remove the entire value package, will create a bunch of errors.
 2. Look at different places where those classes are used and think about strategies on how to solve the problems. These will include : 
   - parser
   - visitors
   - ast2plan translator

##### Parser strategy 

Go over the BNF and create a new set of rules for all the affected elements. Change the corresponding tests.

##### Visitors strategy

Change the abstract visitor plans, then change all concrete visitors.

##### Ast2Plan strategy

TBD