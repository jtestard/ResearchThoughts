# Time Line

1977 : Selinger comes up with a simple, inefficent algorithm for evaluating nested queries which evaluates the entire sub-query for each tuple.

1982 : Kim notes that Selinger's approach is inefficient, and proposes algorithms Nest-N-J and Nest-JA algorithms to rewrite such queries into non-nested join queries. 

1984 : Kiessling found the count bug in Kim's algorithm. He suggests an idea based on OR a predicate to the WHERE clause of the transformed query.

1987 : Ganski notes that the bug revieled by Kiessling is fixable if we allow the (full) outer join operation.

1) The outer join preserves all left hand side (outer query) values whether they match some right hand side value (inner query) or not.

2) This causes another bug which arises when the outer query join attribute contains duplicates, in which case does duplicates are transfered to the count().

1996 : Magic Decorrelation.