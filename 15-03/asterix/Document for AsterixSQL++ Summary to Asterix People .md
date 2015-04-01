### Document for AsterixSQL++ Summary to Asterix People

#### Limitations

 - `FROM (INNER | LEFT OUTER ) JOIN` clauses can only support two items. A third item requires variable unpacking according to present conditions. My take on it is that it is not worthwhile to solve this problem which could be solve by using the `inner join` operator directly in the initial plan.
 - `DISTINCT` is not available because AsterixDB does not suppport complex equality.
 - Algebraically, `outer-unnest` is available in cases where it can next be rewritten into a `left-outer-join`. Otherwise, an error is thrown. Consequences :
   - `LEFT OUTER JOIN` is available on structurally uncorrelated data only. 
   - `OUTER FLATTEN` is not available.
   - `LEFT CORRELATE` on structurally correlated data is not available. 
   - `LEFT CORRELATE` in which the right item is a subquery with a `LIMIT`, `ORDER BY` or `GROUP BY` is unavailable (*).