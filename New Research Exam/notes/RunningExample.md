# Running Example for Research Exam

## Running Exmaples of existing papers

### A Deep Embedding of Queries into Ruby

Ruby Library that allows holistic optimization.

#### Schema

```
CREATE TABLE orders (
	id serial primary key,
	user_id integer NOT NULL,
	item_total integer NOT NULL
);
CREATE TABLE line_items (
	id serial primary key,
	price integer NOT NULL,
	quantity integer NOT NULL,
	order)id integer REFERENCES orders.id NOT NULL
);
```

#### Query In Text

*What would be the cost of granting a discount on the open orders of all high-volume costumers*

#### Program

The program for this paper is provided using Ruby language. Rails uses an ORMs. Comments 

##### Rails Program

```
discount = 20.0/100
high_vol = 10

high_vols = Order.group("user_id")
					.having("[COUNT(user_id) >= ?", high_vol])
					.select("user_id")
# SELECT user_id
# FROM Orders
# GROUP BY user_id
# HAVING COUNT(user_id) >= 10;

open_orders = Order.where("user_id IN (:tc) AND state = :s", 
							{ tc: high_vols.map(&:user_id),
							  s: "0" }])
# SELECT *
# FROM Orders
# WHERE user_id IN (4,8,...,1498,1499) AND state = '0'

items = open_orders.includes(:Line_Item).map(&:line_items).flatten
# SELECT *
# FROM Line_Items
# WHERE order IN (2,3,...,65000)

cost = items.sum {|i| i.price * i.quantity} * discount
```

##### Switch Program

```
discount = 20.0/100
high_vol = 10

high_vols = Order.group_by(&:user_id)
					.select {|u,os| os.length >= high_vol}
open_orders = high_vols.map {|u,os| os.select 
						{|o| o.state == "0"}}.flatten
items = open_orders.map {|o| line_item.in_order(o)}.flatten
cost = items.sum {|i| i.price * i.quantity} * discount

# SELECT SUM(li.price * li.quantity) * 0.2
# FROM ( 
#			SELECT o2.user_id, COUNT(*) AS cnt
#			FROM Orders AS o2
#			GROUP BY o2.user_id
#		) AS oc,
#		Orders AS o1,
#		Line_Items AS li
# WHERE o1.id = li.order_id
# AND o1.state = 'O'
# AND oc.user_id = o1.user_id
# AND oc.cnt > 10
```

#### Query Characteristics

 - Minimal change required on programmer's end.
 - Reduces number of queries from 3 to 1
 - Memory savings because intermediate results do not go through the network.
 - Security strenghtened because we are not using strings "as-is" in the query.
 - It is not known whether switch provides an advantage if a tuple-at-a-time query rewriting is provided.

### Holistic Data Access Optimization for Analytics Reports (FORWARD)

Full-stack framework which users must use in order to reap the benefits.

The example has been slightly simplified by not considering the `date_part` user-defined function.

#### Schema

```
CREATE TABLE nations (
	nation_key serial primary key,
	name text NOT NULL,
	comment text NOT NULL
);
CREATE TABLE customers (
	cust_key serial primary key,
	nation_ref integer REFERENCES nations.nation_key NOT NULL
	address text NOT NULL
);
CREATE TABLE orders (
	order_key serial primary key,
	cust_ref integer REFERENCES customer.cust_key NOT NULL,
	order_year date NOT NULL,
	total_price integer NOT NULL
);
```

#### Query Text

*For each selected nation, provide the nation name and the top 3 years of sales revenue.*

#### Program

The program is given as example in Ruby, and then rewritten to SQL++. We provide both programs here. Given Forward is an MVVM framework, the query is given as part of a template markup. We ignore the template markup here.

##### Ruby

```
Nation.all.each.do |n|
	if session['selected_nations'][n.nation_key] == true then
		aggregates = Order
			.select('order_year, sum(total_price) as sum_price')
			.joins('customer')
			.where('nation_ref = ?', n.nation_key)
			.group('order_year')
			.order('sum_price DESC')
			.limit(3)
	end
end
```

##### SQL++

```
SELECT	n.nation_key, n.name, (
  SELECT order_year,
         sum(total_price) as sum_price
  FROM db.orders AS o,
       db.customers AS c
  WHERE o.cust_ref = c.cust_key
  AND c.nation_ref = nation_key
) AS aggregates
```

##### Query Rewriting Characteristics

 - Requires the program to switch from Ruby to SQL++.
 - Would not be possible in regular SQL, because of nesting. However, SQL++ supports nesting.
 - Framework can push computation to server and apply a set-at-a-time rewriting.
 - Impedance mismatch problem defeated because the coexistence of data structures on the application server and database server is not the programmer's concern, it is handled by the framework.
 - The application logic is also described declaratively in the application program.

 
### Optimizing Database-Backed Applications with Query Synthesis (Status Quo)

Tool which can be used on any existing codebase to apply holistic optimization.

#### Schema

```
CREATE TABLE roles (
	roleId serial primary key
);
CREATE TABLE users (
	userId serial primary key,
	roleId integer REFERENCES role.roleId NOT NULL
);
```

#### Query In Text

List all users whose role corresponds to a role in the role table.

#### Program

The program is written in Java with the Hibernate ORM framework.


##### Hibernate

```
List<User> getRoleUser() {
	List<User> listUsers = new ArrayList<>();
	List<User> users = this.userDao.getUsers();
	List<Role> roles = this.roleDao.getRoles();
	for (User u : users) {
		for (Roles r : roles) {
			if (u.roleId().equals(r.roleId())) {
				U userok = u;
				listUsers.add(userok);
			}
		}
	}
}
```

##### QBS

```
List<User> getRoleUser() {
	List<User> listUsers = db.executeQuery(
		"SELECT u
		 FROM users u, role r
		 WHERE u.roleId == r.roleId
		 ORDER BY u.roleId, r.roleId"
	);
	return listUsers;
}
```

#### Query Rewriting Characteristics

 - Does tuple-at-a-time to set-at-a-time rewriting by inferring first loop invariants and post-conditions, then a SQL translation from those post-conditions and loop invariants.
 - Works on any existing code, by analyzing it. 


## Running Example

Thinking of left-outer-join/group by example.
The running example for the research exam will be a tpc-h inspired example.

Tables


Queries 


