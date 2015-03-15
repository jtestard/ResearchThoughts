Input environment :

```
FacebookMessages :
{ id : 1, sender-location : X, author-id : 1, ...}
{ id : 2, sender-location : X, author-id : 2, ...}
{ id : 3, sender-location : Y, author-id : 2, ...}
FacebookUsers :
{ name : "John", id : 1, ...}
{ name : "Mary", id : 2, ...}
{ name : "Joan", id : 3, ...}
```

Input Queries :

```
FROM FacebookUsers AS fb LEFT CORRELATE
 ( FROM FacebookMessages as fm
   WHERE fb.id = fm.author-id
   GROUP BY fm.sender-location as loc
   HAVING loc = X
   SELECT ELEMENT group
 ) AS fm
SELECT ELEMENT {
	"name" : fb.name,
	"messages" : fm
};
```

Plan :

```
project pVar
assign pVar <- { "name" : fb.id, "messages" : fm' }
soft_unnest fm' <- scan aggVar
subplan { 
	aggregate aggvar <- listify npVar 
	assign npVar <- group
	select loc = X
	group-by loc <- fm.sender-location {
		aggregate group <- group_elem
		nested-tuple-source
	}
	assign group_elem <- { "fb" : fb, "fm" : fm }
	select function-call : eq, args : fb.id = fm.author-id
	unnest fm <- FacebookMessages
	nested-tuple-souce
}
unnest fb <- dataset FacebookUsers
empty-tuple-source
```

Rewritten Plan with left outer join

```
project pVar
assign pVar <- { "name" : fb.id, "messages" : group }
select loc = X
group-by loc <- fm.sender-location {
	aggregate group <- group_elem
	nested-tuple-source
}
assign group_elem <- { "fb" : fb, "fm" : fm }
left-outer-join fb.id = fm.author-id
  unnest fm <- FacebookMessages
  	empty-tuple-source
  unnest fb <- dataset FacebookUsers
	empty-tuple-source
```
What happen if there is no match `fm.author-id` match for a given `fb.id`?

Then a single tuple will be outputted and `fm` will be bound to `null`.

what difference with 


#### Rewriting process

How does the rewriting process work in AsterixDB?

The `PrioritezedRuleController`, `SequentialOnceRuleController`, `SequentialFixpointRuleController` are used to fire rewriting rules. For example, the `PrioritezedRuleController` uses the following algorithm to rewriting each rule until fixpoint one after the other:

```
    @Override
    public boolean rewriteWithRuleCollection(Mutable<ILogicalOperator> root, Collection<IAlgebraicRewriteRule> rules)
            throws AlgebricksException {
        boolean anyRuleFired = false;
        boolean anyChange = false;
        do {
            anyChange = false;
            for (IAlgebraicRewriteRule r : rules) {
                while (true) {
                    boolean ruleFired = rewriteOperatorRef(root, r);
                    if (ruleFired) {
                        anyChange = true;
                        anyRuleFired = true;
                    } else {
                        break; // go to next rule
                    }
                }
            }
        } while (anyChange);
        return anyRuleFired;
    }
```

The `Collection<IAlgebraicRewriteRule> rules` seems to be the place where to add a new rule, say for left outer join rewriting.

The question : is there an operator which can handle `outer-unnest` when it is **not**  rewritten into a `left-outer-join`?

It seems to me that our problem is that there is no equivalent to the `outer-unnest` in their list of physical operators. We'll have to build it ourselves.

As an intermediate solution, we can apply the left-outer-join rewrite rule when it makes sense, and simply throw an error for cases where the outer-unnest cannot be rewritten.

#### Rewriting rule implementation :

We are faced with two problems :

 - implementing the rewriting rule itself.
 - placing it in the list of rewriting rules with respect to dependence.



