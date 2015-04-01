OK,

For the moment, I am trying to write the following rule :

##### Rule #1 : CancelOuterUnnestWhenNestedListify 

Here is what the plan looks like before rewriting :

```
outer-unnest eRes, pRes <- scan collection aggVar
  subplan {
    aggregate aggVar <- listify projVar
     assign projVar <- eIn
       select f(eIn, pIn, eOut, pOut)
         unnest eIn, pIn <- scan collection S
  }
unnest eOut, pOut <- scan collection R
```

Here is what the plan after rewriting :

```
left-outer-join f2(eIn, pIn, eOut, pOut)
   unnest eIn, pIn <- scan collection R
   unnest eOut, pOut <- scan collection S
```

where `R, S` are one of `dataset`, `complex constant` or `subquery`.

Here is the same rule using the SQL++ language directly :

Before rewriting : 

```
from R as eOut at pOut
left correlate
( from S as eIn at pIn
  where f(eIn, pIn, eOut, pOut)
  select element eIn
) as eIn
```

After rewriting :

```
from R as eOut at pOut
left outer join S as eIn at pIn
on f(eIn, pIn, eOut, pOut)
```

It seems to me that it should be in `edu.uci.ics.asterix.optimizer.rules`, but I haven't found a similar rule yet in that package. The `CancelUnnestWithNestedListifyRule.java` which you told me to look at is actually pretty different.

Best,

Jules


