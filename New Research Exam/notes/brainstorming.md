**Impedance mismatch** : logical and physical between the data storage on a database and in a in-memory program

Impedence mismatch is cayse 

Poor performance in database applications are due to :

 1. Iterative execution of queries within a procedural loop structure 
   - Synchronous blocking leads to inefficiencies
 - Straightforward translation of operations on persistent objects (for example in the context of ORMs)
 
Analytics reports involve nested (1) and aggregated results.



Example without optimization :

```
int sum = 0;
List categories = new ArrayList();
ResultSet rs = execute("SELECT * FROM categories");
while (rs.next()) categories.add(rs.getInt("id"));
while (!categoryList.isEmpty()) {
	int category = categoryList.removeFirst();
	rs = execute("select count(partkey) from part p" +
		"where p.category=" + category);
	int count = rs.getInt("count");
	sum += count;
}
```

Example with optimization :

```
int sum = 0;
List categoryCounts = new ArrayList();
ResultSet rs = execute(
	"SELECT c.id, count(partkey)
	FROM category c LEFT OUTER JOIN part p
	ON c.id = p.category
	GROUP BY c.id");
while (!CategoryCounts.isEmpty()) {
	count = CategoryCounts.removeFirst();
	sum += count;
}
```