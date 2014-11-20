# SQL++ AsterixDB Wrapper and Distribution

## Project Schedule and Deadlines
 - *October 17th 2014*: AsterixDB use cases slides deadline.
 - *October 19th 2014*: Distributed Normal Form Discussion.

## Tasks
There are two main tasks required to serve AsterixDB data to the Forward query processor :

 - **AsterixDB Virtual View**: Defines what kind of plans can be sent from Forward processor to the underlying Asterix datbabase*. More specifically, it defines :
   - Supported SQL++ operators/functions
   - AsterixDB-specific plan normal form
 - **Source Annotation Algorithm**: describes how does the distribution algorithm uses the virtual view to construct a AsterixDB annotated query plan.
 - **AsterixDB Wrapper**: translates the AsterixDB annotated query plan into a AQL or SQL++ query.

*: the concept of virtual views shown in the SQL++ paper differs from this definition.   
## Specification

**Input**:

A source-agnostically optimized SQL++ query plan.

**Output**:

A SQL++ or AQL query to send to AsterixDB.

=======================

## AsterixDB Use Cases

These use cases present examples of queries that can be submitted to a Forward query processor with two underlying sources:

 - a PostgreSQL database
 - a AsterixDB database

We will develop three examples :

 - AsterixDB only
 - AsterixDB + Forward in memory
 - AsterixDB + PostgreSQL

### Context

Restaurant review service dataset.

**AsterixDB Dataset**:

	drop dataverse RestaurantReviewDemo if exists;
	create dataverse RestaurantReviewDemo;
    use dataverse RestaurantReviewDemo;
	create type UserType as closed {
    	user_info : {
    		name : string,
    		age : int32,
    		location : string,
    		interests : {
    			venue_type : {{ venue : string }},
	    		food_style : {{ category : string }}
    		}
    	},
	    user_key : int32
	};
	create type ReviewType as closed {
		user_key : int32,
		review_key : int32,
		rating : int32,
		comments : string,
		venue_name : string,
		venue_type : string,
		food_style : string,
	};
	
    create internal dataset Users(UserType) primary key cust_key;
    create internal dataset Reviews(ReviewType) primary key order_key;
    insert into dataset Customers([
    	{
    		"user_info" : {
    			name : "John Smith",
    			age : 32,
    			location : "La Jolla, CA",
    			interests : {
    				venue_type : {{"bar", "restaurant"}},
    				food_style : {{"sushi", "tacos"}}
    			}
    		},
    		"user_key" : 0
    	},
    	{
    		"user_info" : {
    			name : "Angela Lopez",
    			age : 21,
    			location : "Pacific Beach, CA",
    			interests : {
    				venue_type : {{"bar", "nightclub"}}
    			}
    		},
    		"user_key" : 1
    	},
    ]);
    insert into dataset Orders([
    	{
    		"user_key" : 0,
    		"review_key" : 0,
    		"rating" : 2,
    		"comments" : "...",
    		"venue_name" : "Edo Sushi",
    		"venu_type" : "restaurant",
    		"food_style" : "sushi"
    	},
    	{
    		"user_key" : 1,
    		"review_key" : 1,
    		"rating" : 5,
    		"comments" : "...",
    		"venue_name" : "Kyoto Sushi",
    		"venu_type" : "restaurant",
    		"food_style" : "sushi"
    	},
    	{
    		"user_key" : 0,
    		"review_key" : 2,
    		"rating" : 3,
    		"comments" : "...",
    		"venue_name" : "La rosa de oro",
    		"venu_type" : "restaurant",
    		"food_style" : "Tacos"
    	},
    	{
    		"user_key" : 1,
    		"review_key" : 3,
    		"rating" : 5,
    		"comments" : "...",
    		"venue_name" : "Tutti quanti",
    		"venu_type" : "restaurant",
    		"food_style" : "italian"
    	}
    ]);


### Case 1 : Query can be answered by AsterixDB alone

What is the average rating for reviews for each food style?

	SELECT R.food_style as style, avg (R.rating) AS avg_rating
	FROM Reviews AS R
	GROUP BY R.food_style

We just send the entire query over to AsterixDB. 

### Case 2 : Query cannot be done by AsterixDB alone

We want to know how well users indicate their interests. In particular, we want to know how many of the reviews they write correspond to their declared food interests. For each user's food interest, we count how many reviews that user wrote that matched that interest.

	SELECT U.user_info.name, fs, COUNT(R.review_key)
	FROM Reviews AS R
	JOIN OUTER FLATTEN (
		Users AS U,
		U.user_info.interests.food_style AS fs
	)
	ON U.user_key = R.user_key AND fs = R.food_style
	GROUP BY U.user_info.name, fs

Notice that if we used INNER FLATTEN, Angela would not show up in the records. OUTER FLATTEN, on the other hand, is not supported by AsterixDB.

### Case 3 : Query done by AsterixDB + SQL

The company has decide to compensate reviewers who write good quality reviews. All reviews are given price tags. Reviewers get compensated the sum of their price tags by the end of the month. Reviews that haven't been analyzed or not been considered good enough are given a price tag of 0. PriceTag data is stored in a SQL database (PostgreSQL).

**SQL dataset**:

    CREATE TABLE PriceTag (
        pt_key int primary key not null,
        user_key int not null,
        review_key int not null,
        amount double not null,
        timestamp timestamp default current_timestamp
    )

    INSERT INTO PriceTags(pt_key, user_key, review_key, amount)
    VALUES
        (0,0,0,1.23),
        (1,0,1,1.55),
        (2,0,2,3.53),
        (3,1,3,0.0)
    );

#### Case 3.a

What is the average compensation for each rating grade (rating grades are integers from 1 to 5)?

	SELECT R.rating, AVG(P.amount)
	FROM Reviews AS R
	JOIN PriceTags AS P
	ON P.review_key = R.review_key
	GROUP BY R.rating

In this case, the inner join can be done on the mediator.

#### Case 3.b

What is the average compensation for each rating grade of John Smith (user_key=0) ?

	SELECT R.rating, AVG(P.amount)
	FROM Reviews AS R
	JOIN PriceTags AS P
	ON P.review_key = R.review_key
	WHERE P.user_key = 0
	GROUP BY R.rating

In this case, there is a great incentive to have the inner join done in PostgreSQL. We can do this by doing an apply plan rewriting.

========================
### Email Exchange with Yannis

**Jules**:

Hello Yannis,

I have a questions about the MapR slides.

I have seen that on the SQL++ survey paper (Figure 1 Page 3) we have a set of SQL++ virtual views for each wrapper. 

	Conceptually, each database (be it SQL or non-SQL) a    ppears to the client as a set of SQL++ virtual views.

On the other hand, in the MapR slides (slide 12), we have a single SQL++ virtual view per data base.

Did the semantics of a SQL++ virtual view change between the paper and the slides?

==============================

**Yannis**:

no, just the slideware changed ;-)

We have not been clear on the SQL++ paper on the naming convention of sources.

The term "view" is not defined now. If you wish a view to be a collection of named values then each wrapper exports a view. The view could have a named value "Customers", another named value "orders" etc.

If you want to associate "view" with a single top-level named value, then the wrapper exports "viewS", where one view is the Customers, another is the Orders etc.

I'm leaning towards the "views"

==============================

**Jules**:

Ok, but in both cases a SQL++ virtual view defines what data can be obtained from the source (what collection, what named value…).
An alternative approach would be to have a SQL++ virtual view define how that data can be obtained from the source, i.e. what kind of queries can be used on the source. The SQL++ virtual view thus defines the query capabilities of the underlying source.

### Draft and ideas 

 - Normal Form for plans accepted by the AsterixDB wrapper