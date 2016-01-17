## Examples

 - Prove each rewriting is correct.
 - For each rewriting:
   - Build theoretical cost model using simplest assumptions first. CHECK
   - Find one example which is beneficial for each rewriting
   - Find one example which is detrimental (if found, then don't always apply the rewriting)
 - Clarify the key assumption

#### 

#### Key assumption clarification

A key is not required for rewritings to work, but if the key is present, a distinct is not necessary.

#### Optimizations

 - Scalar optimization: Push some extra computation to the database by allowing group by and left outer join to be pushed if they return scalars, only to nest them in middleware


```

```