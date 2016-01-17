```java
public static List getNationsForKeys(List<Integer> selectedKeys) {
	List nations = session.createQuery("SELECT * FROM Nation");
	List result = new ArrayList();
	for (Nation nation : nations) {
	   if (selectedKeys.contains(nation.getKey()) {
	   	result.add(nation);
	   }
	}
	return result;
}
```

```java
public static getNationsForKeys(List selectedKeys) {
	return session.createQuery(
		"SELECT n.nation_key, n.name" +
		"FROM Nations n, selectedKeys s" +
		"WHERE n.nation_key = s.key", selectedKeys
	)
}
```

```SQL
CREATE TABLE selectedKeys (
	KEY INTEGER
);
```