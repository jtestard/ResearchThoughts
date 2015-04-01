## Outer Unnest Operator

### Previous elements of conversation on Outer Unnest Operator

Most of the following comes from an email conversation which occured on Tuesday February 17th.

##### Soft/Outer unnest operator description

Implement a new Algebricks logical operator called **outer_unnnest** to be used in the context of SQL++ left outer join. The semantics of that operator are as follows :

`outer_unnest s at p <- S (R)` : The `outer_unnest` operator has the following attributes : 

 - An input operator `R` : the tuples outputted by `R` are the input tuples of `S`.
 - An input expression `S`: this expression must evaluate to a collection of values  or a dataset.
 - An element variable `s`.
 - A positional variable `p` which may be null.

For each tuple `r` of the collection `C` produced by `R` and for each element `v` of the collection `C'` resulting from the evaluation of `S` (with `i` the integer corresponding to the position of `v` in `C'`), it outputs one tuple `b` which is the concatenation of the variable bindings of `r` and the new bindings `s : v, p : i` (or just `s : v` if `p` is null).

If `S` is empty when considering some `r` in `R`, then a single tuple is outputted which is the concatenation of the variable bindings in `r` and the new binding `s : null`.

Implementing this operator will also require integrating it in the rewriting rules of the Asterix optimizer.

##### Yannis suggestion

So, the rule you refer to here is the one that turns soft_unnest into left outerjoin. I recap that we want this rule because ASTERIX already has the work on optimizing plans with left outerjoin.

Notice that decorrelating the S requires a case analysis for the presence of GROUP BY in the optional side S. Consider the following query where R is not correlated to the variable l introduced by the left side. Hence the query is a good candidate for decorrelation and introduction of LEFT OUTERJOIN. The catch is the bruhaha with the requisite flags that distinguish the kinds of nulls.

```
FROM left_item AS l LEFT CORRELATE
 ( FROM R as r
   WHERE w(r, l)
   GROUP BY e_1(r,l) AS v_1 ... e_n(r,l) AS v_n
   HAVING h(v_1,...v_n, group)
   SELECT ELEMENT f(v_1,...v_n, group)
 ) AS r'... 
```

rewrite the above to become a LEFT OUTERJOIN between two uncorrelated expressions. (Preferably without looking at the FORWARD documents :) )
It is very tricky! Try it out yourself.

Does every logical operator have a physical counterpart?

##### Variable packing/unpacking



### Objectives

#### Case Analysis

 1. Find out what are the different situations in which a left outer join operator can appear and what will matter in each case in terms of rewriting.

#### Implementation

 1. Figure out if it is possible to implement the outer unnest from existing physical operators.
 2. If yes, then do so, thus gaining an unoptimized outer unnest operator.
 3. If not, figure out what are the conditions to obtain the outer unnest.

### Case Analysis

missing

### Implementation 

##### Is it possible to implement the outer unnest from existing physical operators

Look at rewriting descriptions through the code and the AsterixDB architecture paper[1]. From those figure out the process of rewriting from the initial logical plan to the optimized logical plan. 
The process should be similar to that of the Aql AST to initial plan. To understand this process, use a simple query and understand how it gets rewritten. A good initial could be one that involves an inner join :

```
select user.name as user, message as message
from FacebookUsers as user
join FacebookMessages as message
on user.id = message.author-id;
```

Once this process is done, try to imagine how the process would go if the query was changed to :

```
select user.name as user, message as message
from FacebookUsers as user
left outer join FacebookMessages as message
on user.id = message.author-id;
```

##### Reading conclusions

The AsterixDB paper[1] does not go into detail about rewriting rules, but does point out that there is a direct correspondance between the optimized logical plan and the Hyracks Job specification. 

The Hyracks Job Specification is a DAG where nodes are Hyracks Operator Descriptors (HOD) and edges are ConnectorDescriptors (CD). The micro-operators of an HOD are (static) physical operators in the literature.

From code inspecion, the `LeftOuterJoinOperator` logical operator seems a good candidate. Indeed, if we "cheat" and use the left outer join operator directly in the initial plan, we are able to get the proper left outer join output.

However, this does not allow us to rewrite any instance of `left correlate` into `left-outer-join` as of yet. For this, we need to introduce the `OuterUnnestOperator`. The requirement becomes now figure out how to rewrite queries with `OuterUnnestOperator` into queries with `LeftOuterJoinOperator`.


##### Working out stuff

 - new logical operator `OuterUnnestOperator` created. DONE
 - show we know how to get the right output by "cheating", making the rewriting a part of the AST (by not rewriting left outer join to left correlate). DONE
 - once we know how to get the right output, do it right using a rewriting. 



----------
[1] : ASTERIX, towards a scalable, semistructed data platform for evolving-word data models.