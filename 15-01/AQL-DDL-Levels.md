### Email to Asterix Guys about presentation details

Hello Mike,

Sure I do! I’ll send a message to Ian. 

In the meantime, I have a question to ask.

Recalll what we agreed upon for statements exposed on the SQL++ endpoint :

 - We use SQL++ syntax for queries only and use AQL syntax for all other statement types.

For this purpose, we extend the exisiting JavaCC-based SQL++ parser (SQLPP.jj) by copying over relevant parsing rules from the existing AQL parser (AQL.jj) [1].

I would like a little more specifics on how this will play out. As a reference for this conversation, you may look at :

 - The grammar for AQL : https://asterixdb.ics.uci.edu/documentation/aql/manual.html
 - The grammar for SQL++ : https://github.com/jtestard/asterixdb-sqlpp


Consider the following categories of programs a user would write:

#### CATEGORY 1 

Programs consisting only of `SQLPPQuery` and `DataverseDeclaration` statements.

Example program in category 1 :

```
use dataset TinySocial;

select fb.alias from FacebookUsers as fb;

select fb.alias from FacebookUsers as fb where fb.id = 8;
```

#### CATEGORY 2

Programs consisting only of : 

 - AQL statements whose production **do not** contain **arbitrary** AQL expressions.* 
 - Statements from category 1.

\* : arbitrary AQL expressions may be any expression matched by the `Expression` production (see AQL grammar documentation).

Example program in category 2 :

```
create dataverse TinySocial;

create type FacebookUserType as closed {
  "id" :         int32,
  "alias" :      string,
  "name" :       string,
  "user-since" : datetime,
  "friend-ids" : {{ int32 }},
  "employment" : [ EmploymentType ]
}

create internal dataset FacebookUsers(FacebookUserType) primary key id;

create external dataset Lineitem('LineitemType) using hdfs (
  ("hdfs"="hdfs://HOST:PORT"),
  ("path"="HDFS_PATH"),
  ("input-format"="text-input-format"),
  ("format"="delimited-text"),
  ("delimiter"="|"));

create index fbAuthorIdx on FacebookMessages(author-id) type btree;  
```

#### CATEGORY 3

Programs consisting only of :

 - Insert/Delete statements with arbitrary AQL expressions*.
 - Statements from category 2.

Example program from category 3 :

```
use dataverse TinySocial;

insert into dataset FacebookUsersCopy (
	for $fb in dataset FacebookUsers return $fb
);

delete $fb from dataset FacebookUsers where $fb.id = 8;
```

Programs from categories up to 3 are straigthforward to parse with the method described in [1], because each statement can be fully parsed into an SQL++ AST (for SQL++ queries) or a AQL AST (for all other statements). There is no ambiguity as to which AST to use when the parser encounters any statement.

However, category 3 introduces some AQL Query syntax within the `Insert` and `Delete`.

#### CATEGORY 4

Program consisting only of :

 - AQL Query statements*.
 - Statements from category 3.

Example program from category 4 :

```
use dataverse TinySocial;

for $user in dataset FacebookUsers where $user.id = 9 return $user;

select message from FacebookMessages as message where message.author-id = 8;
```

Programs from category 4 require some extra thinking because they introduce at least one ambiguity. Consider the statement :

```
"Hello World!";
```

Should it be parsed as the AQL AST?

```
Query:
LiteralExpr [STRING] [Hello World!] 
```

Or should it be parsed as the SQL++ AST?

```
{
  "query":"Hello World!"
}
```


#### CATEGORY 5

Program consisting only of :

 - Any arbitrary AQL and SQL++ expression*.
 - Statements from category 4.
 
\* : anywhere where the `Expression` symbol is used on the right-hand side of a production rule in the AQL grammar specification, a `SQLPPExpression` can be used instead (and vice versa).

Example program in category 5 :

```
use dataverse TinySocial;

select message
from FacebookMessage as message, 
	(for $user in dataset FacebookUsers return $user) AS user
where message.author_id = user.id;

insert into dataset FacebookUsersCopy (
	select fb from FacebookUsers as fb
);
```

I don't know exactly how difficult it will be to achieve correctness with programs in this category, but it will be very difficult.

Which category of programs should we aim to support?

Best,

Jules Testard

==========================================================================================

Agreed, but this doesn’t directly answer my question. 

I am going to suggest one more category :

#### CATEGORY 3.b

Programs consisting only of :

 - Statements from category 2.
 - Insert/Delete statements with arbitrary SQLPP expressions* [A].

\* : arbitrary SQL++ expressions may be any expression matched by the `SQLPPExpression` production (see AQL grammar documentation).

By statement [A], we mean that the grammar production for `Insert` and `Delete` statements from AQL is changed to the following in the SQL++ endpoint:

```
InsertStatement ::= "insert" "into" "dataset" QualifiedName SQLPPQuery
DeleteStatement ::= "delete" SQLPPVariable "from" "dataset" QualifiedName ( "where" SQLPPExpression )?
```

Example program from category 3.b :

```
use dataverse TinySocial;

insert into dataset FacebookUsersCopy (
	select fb from FacebookUsers as fb
);

delete fb from dataset FacebookUsers where fb.id = 8;
```

Programs from categories up to 3.b are also straigthforward to parse with the method described in the previous email, and do not add any AQL query syntax. However, from a user point of view, we still have this strange "dataset" key word we should be adding sometimes and sometimes not. 

I know have two questions for you :

 - Is the concept of category of programs used here clear enough to understand what would the eventual SQ++ endpoint look like?
 - Is category 3.b satsfying or is there still "something" missing from the picture?


