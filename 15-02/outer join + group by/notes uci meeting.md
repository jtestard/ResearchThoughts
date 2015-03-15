Notes UCI Meeting :

 - implement soft unnest (left outer join). Look first at the easy cases, then try the hard one with the aggregate correlated left outer join using the let clause solution coupled with inner clause.
   - coordinate with Yingyi (make a design).
 - Ask Yingyi for rewriting rules that need to be edited for the unnest operator.
 - int64 is the default. morph into asterix values
 - group by can be created using let clause simulation.
 - wewe.
 - need to figure out something about the minus sign operator.
 - Ask yannis about good papers on federated queries.
 
 

On our Friday February 13th UCI meeting, we were able to make progress on severals issues :

### Major issues

##### GroupBy Operator

Consider the following "complex" query :

*Get the name of all Facebook users who sent messages from location X and return them as a bag named "results".*

and its SQL++ equivalent (schema for the query is available [here](https://asterixdb.ics.uci.edu/documentation/aql/manual.html)) :

```
from FacebookUsers as fb
join FacebookMessages as fm
on fb.id = fm.author-id
group by fm.sender-location as loc
having loc = X
select element {
   "results" : (from group as g
               select element g.fb.name)
} 
```

This query can be expressed in AQL as follows :

```
for $fb in dataset FacebookUsers
for $fm in dataset FacebookMessages
where $fb.id = $fm.author-id
let $group := { "fb" : $fb, "fm" : $fm }
group by $loc := $fm.sender-location with $group
where $loc = X
return {
  "results" : for $g in $group
  	          return $g.fb.name
};
```

Thanks to the powerful rewriting capabilities of the Asterix optimizer, this translation is good enough to simulate the SQL++ group by operation.

##### Left Outer Join

Implement a new Algebricks logical operator called **soft_unnnest** to be used in the context of SQL++ left outer join. The semantics of that operator are as follows :

`soft_unnest s at p <- S (R)` : The `soft_unnest` operator has the following attributes : 

 - An input operator `R` : the tuples outputted by `R` are the input tuples of `S`.
 - An input expression `S`: this expression must evaluate to a collection of values  or a dataset.
 - An element variable `s`.
 - A positional variable `p` which may be null.

For each tuple `r` outputted by `R`, the operator iterates over the collection or dataset in the context of `r` and for each element `v` of `S` (with `i` the integer corresponding to the position of `v` in `S`), it outputs one tuple `b` which is the concatenation of the variable bindings of `r` and the new bindings `s : v, p : i` (or just `s : v` if `p` is null).

If `S` is empty when considering some `r` in `R`, then a single tuple is outputted which is the concatenation of the variable bindings in `r` and the new binding `s : null`.

Implementing this operator will also require integrating it in the rewriting rules of the Asterix optimizer.

### Minor issues

##### Asterix Data Types

Asterix uses more specific data types than SQL++. In particular, Asterix uses six datatypes to represent numbers : `int8`, `int16`, `int32`, `int64`, `float`, `double`, while SQL++ uses only one : `number`. The question then naturally asks itself : 

*If a number is used within a SQL++ query, which Asterix datatype should be used to represent that number?*

**Suggested Solution** use Asterix's data types and copy Asterix's strategy : when parsing a query, implicitly cast any integer found into an `int32` and any non-integer found into a `double`. Explicit casting to other datatypes can be achieved using builtin functions.

##### Minus sign operator

The minus sign `-` symbol in Asterix is allowed in attribute names. This is likely to cause a parsing conflict with the use of the `-` operator in the context of the substraction operation. Asterix avoids this problem by having a `$` in front of its variables (which SQL++ does not have). A solution must be found to handle this case in the context of SQL++.

**Suggested solution** when constructing tuple navigation (or field accesses in Asterix linguo), we could consider both following syntax acceptable : 

```
tuple.attribute
tuple."attribute"
```
When dealing with `-` symbol in an attribut name, the latter syntax can still be used.

##### Dataset keyword

The `dataset` keyword in the context of SQL++ is a little superfluous and should be removed for SQL backwards compatibility purposes.