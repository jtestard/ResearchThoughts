### Dynamic Dispatch on Asterix API Framework

Dynamic dispatch : replacing case analysis by polymorphism. 

(AQL/SQLPP Query) accepts an (AQL / SQLPP Visitor)

The AQL/SQLPP query have a superclass called IQuery which they can use

We can create IExpressionVisitor as a super interface for the AQL/SQLPP Visitors.

Only problem, such a class would create a dependence between the aql and sqlpp packages.

Full dynamic dispatch is not possible, because it would require making the asterix-sqlpp classes available from within the asterix-aql package which violates the dependence tree between those packages. The only solution to make this work would be to merge the asterix-aql and asterix-sqlpp modules, which might/might not be a good idea.

We can at least avoid the use of instance_of using the QueryLanguage enum.

```
if (q != null) {
    if (q instanceof Query) {
        ((Query) q).accept(new AQLPrintVisitor(conf.out()), 0);
    } else if (q instanceof SQLPPQuery) {
        ((SQLPPQuery) q).accept(new SQLPPPrintVisitor(conf.out()), 0);
    } else {
        throw new AsterixException("Query is not an AQL or SQL++ query!");
    }
}
```

```
if (q != null) {
	q.accept(q.makePrintVisitor(conf.out()), 0);
}
```

```
@Override
public <R, T> R accept(IExpressionVisitor<R, T> visitor, T arg)
            throws AsterixException {
    return visitor.visitOrderByClause(this, arg);
}
```

To build 