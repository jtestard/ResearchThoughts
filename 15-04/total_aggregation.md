Hello all,

I have realized that it is impossible to express the following SQL query in SQL++ using the semantics described in the reference implementation paper :

```
SELECT COUNT(*)
FROM Nations as n;
```
The reason simply being that the SQL++ semantics would consider this query as a syntactic sugar for :

```
SELECT COUNT(group)
FROM Nations as n;
```

but there are no `group`s generated in the case of total aggregation.

An extension which would allow to fix this problem would be :


#### 1. Allow grouping by nothing

We introduce a special value for the group by called `nothing` which can be used an argument for the `GROUP BY` operator instead of a set of grouping expressions and their corresponding variables.

When the `nothing` keyword is used on a `GROUP BY` operator, a single binding tuple is outputted with a single variable called `group`. All input binding tuples of the environment of the enclosing query are grouped together in a single collection bound to `group`.

###### Example

An example is provided with the environment being prepended by `>>>` symbols.

````
>>> { Nations : {{
>>> 	{ name : "USA", continent : "america" },
>>>		{ name : "China", continent : "asia" } 
>>> }} }
FROM Nations as n
>>>	{ n : { name : "USA", continent : "america" } }
>>>	{ n : { name : "China", continent : "asia" } }
GROUP BY nothing
>>>	{ group : {{ 
>>>		{ n : { name : "USA", continent : "america" } }
>>>		{ n : { name : "China", continent : "asia" } }
>>> }} }
SELECT COUNT(group) as count;
>>> 2
````

#### 2. Create a new syntactic sugar rewriting

The running example query can then be considered as syntactic sugar for:

```
SELECT COUNT(group)
FROM Nations as n
GROUP BY nothing;
```