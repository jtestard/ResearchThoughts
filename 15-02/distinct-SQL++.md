Implementing distinct

It seems to me that the distinct operator, as it appears in SQL++, cannot be easily translated in the context of AQL. The Asterix SQL++ deals with mapping constructs SQL++ into some kind of AQL equivalent. Unfortunately, AQL only support a constrained form of distinct, it can only distinguish one field at a time, since it does not support complex equality. Thus it seems unreasonable to implement `distinct` in the context of Asterix SQL++.

