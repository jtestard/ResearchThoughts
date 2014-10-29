#SQL++ Concepts

## Basic Concepts

 - **Variable** : may be *relative* or *absolute*.
 - **Parameter** : has a *term* which corresponds to the data it represents. The parameter can have one of two instantiation methods :
   - COPY : value of the term 
   - ASSIGN : value of the term of the parameter is determined at run-time.

## Advanced Concepts

Here are a few SQL++ concepts described by example.

### Flatten

**SQL++ Type** :

Here is the SQL++ type we will use for our example.

	clothes : {{
		{
			name : string,
			sizes : {{ size : int }},
			brands : {{ name : string }}
		}
	}}

**Input** :

	clothes : {{
		{
			name : "shoes",
			sizes : {{9,10,11}},
			brands : {{"aldo","adidas"}}
		},
		{
			name : "pants",
			brands : {{"zara","H&M"}}
		}
	}}
	

####Inner Flatten

**Query**:

	SELECT C.name, size
	FROM INNER FLATTEN (
		clothes AS C,
		C.sizes as size
	)

**Output**:
	
	{{
		{name : "shoes", size: 9},
		{name : "shoes", size: 10},
		{name : "shoes", size: 11}
	}}
	
####Outer Flatten

**Query**:

	SELECT C.name, size
	FROM OUTER FLATTEN (
		clothes AS C,
		C.sizes as size
	)

**Output**:

	{{
		{name : "shoes", size: 9},
		{name : "shoes", size: 10},
		{name : "shoes", size: 11},
		{name : "pants", size: null}
	}}