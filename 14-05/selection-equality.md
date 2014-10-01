#Selection Equality

## The problem
 - We focus on selection because this is commonly the most selective type of operator, where pushing down work would likely bring the most benefit. 
 - We focus on equality because this is the most common type of selection predicate.
   - Less-than comparison is similar but introduces slightly more complexity.
 - Consider join-less queries using a single remote source S, where P is a set of predicates in CNF.
 - We want to push down as much work as possible to the source. 

### The process
 
 - We decompose the selection predicates into   

 - Any predicate pushed down to the source should not result in failure, as this could prevent valid tuples to be processed by the middleware.
   - Rule of thumb : the selection at the source should return an error *if and only if* the same error is returned when the selection is processed at the middleware. 
 - Parenthesis : Method presented here may not be easily applicable to CQL (CQL disallows any comparisons that isn't between two scalars).
 - All of the examples are written in SQL++. The conversion from SQL++ to the source language is the responsibility of the source wrapper.
 - Note that we do not look at the Hive '<=>' and JSONiq 'deep-equal' operators. We assume that the source wrapper will choose the most appropriate operator when translating SQL++ into Hive or JSONiq syntax. 
   - Example : A comparison between complex values `a=b` in SQL++ would be translate into `deep-equal(a,b);` in JSONiq. 


## Query Rewriters
We now present the different rewriters used for selection equality. For each rewriter, we present its behavior when 1) comparing a variable with a literal, 2) comparing  a variable with another variable. Note that comparing two literals can be reduced to 1) by aliasing the first literal (plus it doesn't really make sense).  

###Complexity Rewriter
Fact sheet :

 - Reduces complex equality to its minimum using atomic predicates
 - Introduces path navigation.
 - Assumes paths are accessible.
 - Assumes types are correctly matched.
 
It is assumed that most (if not all) sources are able to compare scalar values of the same type. The complex rewriter simplifies
equality between complex values by using path navigation to compare values. 

#### Variable compared with literal 

Sample input :

	user.profile = 
	{ 	name : 'Jules Testard',
		age : 22,
		birthdate : 21/10/1991,
		address : {
			mumber : 3420,
			street : 'Lebon Drive',
			apartment : '3204',
			zipcode : 92122,
			state : 'California'
		}
		phoneNumbers : [
			0607588079
			8589979311
		],
		hobbies : {{
			{ 	
				'category' : 'sport',
				'occupation' : 'surfing'
			}
		}},
		chatHistory : (
			timestamp('1014-03-12T20:00:00') : 'Hello!',
			timestamp('1014-03-12T20:00:39') : 'How are you today?',
		)
	}


Sample output :

	user.profile.name = 'Jules Testard' AND
	user.profile.age = 22 AND
	user.profile.birthdate = 21/10/1991 AND
	user.profile.address.number = 3420 AND 
	user.profile.address.street = 'Lebon Drive' AND 
	user.profile.address.apartment = '3204' AND 
	user.profile.address.zipcode = 92122 AND
	user.profile.address.state = 'California' AND
	user.profile.address.attrs() = {{'number','street','apartment','zipcode','state'}} --bound check  
	user.profile.phoneNumbers[1] = 0607588079 AND
	user.profile.phoneNumbers[2] = 8589979311 AND
	user.profile.phoneNumbers.length() = 2 AND --bound check
	user.profile.hobbies = {{ {'category' : 'sport','occupation' : 'surfing'} }} AND 
	user.profile.chatHistory-> timestamp('1014-03-12T20:00:00') = 'Hello!' AND
	user.profile.chatHistory-> timestamp('1014-03-12T20:00:39') = 'How are you today?' AND
	user.profile.chatHistory.key_set() = {{ timestamp('1014-03-12T20:00:00'), timestamp('1014-03-12T20:00:39') }} AND --bound check
	user.profile.attrs() = {{ 'name', 'age', 'birthdate', 'address', 'phoneNumbers', 'hobbies', 'chatHistory' }} --bound check
	
Notice that bound checks for tuples are required in case of open types only.
 
#### Variable compared with variable 

Assume the following query :

	SELECT U1.user
	FROM S.users AS U1, S.users AS U2
	WHERE U1.user.profile.address = U2.user.profile.address AND U1.user.profile

Option 1 :
Assuming that the source relation is a closed type and a schema is available, then path navigation for tuples can be used according to the schema :

	U1.user.profile.address.number = U2.user.profile.address.number AND 
	U1.user.profile.address.street = U2.user.profile.address.street AND 
	U1.user.profile.address.apartment = U2.user.profile.address.apartment AND 
	U1.user.profile.address.zipcode = U2.user.profile.address.apartment AND
	U1.user.profile.address.state = U2.user.profile.address.apartment

Notice that the bound check is not required given the closed type assumption. 
However when comparing two variables, path navigation within arrays or maps is not possible.  

Option 2 :

Yield and let the middleware handle this type of equality. 

### Type checking rewriter
Fact sheet :
 
 - Assumes complex value rewriting has already occurred.
 - Assumes paths are accessible.
 - Introduces type checks and only execute comparisons if types match.
 - Complex values : bag contents cannot be type-checked, while arrays, maps and tuples can.  
 - Assumes elements are either scalars or bags (because arrays, maps and tuples can be navigated as shown above).
 
####Variable compared with literal

 - Each navigation path which should evaluate to a scalar (literal is a scalar) will be type-checked.
 - Each type check is placed right before the navigation path.
 - Each navigation which should evaluate to a bag is not type-checked. Reasons :
   - Type checking of the contents of a bag cannot be accurately expressed in SQL++ because of lack of navigation within bags.
   - The only languages which support complexity between bags are Jaql, JSONiq, MongoDB, MongoJDBC and N1QL, and none of these languages return an error in case of type mismatch.
 - Bounds for arrays are known to be integers, therefore no type checking is required.
 - Sample input is identical to output from previous rewriter.
	
Sample output :

	type(user.profile.name) = string AND
	user.profile.name = 'Jules Testard' AND
	type(user.profile.age) = number AND
	user.profile.age = 22 AND
	type(user.profile.birthdate) = date AND
	user.profile.birthdate = 21/10/1991 AND
	type(user.profile.address.number) = number AND
	user.profile.address.number = 3420 AND 
	type(user.profile.address.street) = string AND
	user.profile.address.street = 'Lebon Drive' AND
	type(user.profile.address.apartment) = string AND 
	user.profile.address.apartment = '3204' AND 
	type(user.profile.address.zipcode) = number AND
	user.profile.address.zipcode = 92122 AND
	type(user.profile.address.state) = string AND
	user.profile.address.state = 'California' AND
	user.profile.address.attrs() = {{'number','street','apartment','zipcode','state'}} AND --type check not required
	type(user.profile.address.phoneNumbers[1]) = number AND
	user.profile.phoneNumbers[1] = 0607588079 AND
	type(user.profile.address.phoneNumbers[2]) = number AND
	user.profile.phoneNumbers[2] = 8589979311 AND
	user.profile.phoneNumbers.length() = 2 AND
	user.profile.hobbies = {{ {'category' : 'sport','occupation' : 'surfing'} }} AND --type check not required 
	type(user.profile.chatHistory-> timestamp('1014-03-12T20:00:00')) = string AND
	user.profile.chatHistory-> timestamp('1014-03-12T20:00:00') = 'Hello!' AND
	type(user.profile.chatHistory-> timestamp('1014-03-12T20:00:39')) = string AND
	user.profile.chatHistory-> timestamp('1014-03-12T20:00:39') = 'How are you today?' AND
	user.profile.chatHistory.key_set() = {{ timestamp('1014-03-12T20:00:00'), timestamp('1014-03-12T20:00:39') }} AND --type check not required
	user.profile.attrs() = {{ 'name', 'age', 'birthdate', 'phoneNumbers', 'hobbies', 'chatHistory' }} --type check not required

 - Note that there is no official syntax in SQL++ for type checking. The function `type(value)` used here returns the SQL++ type of the input `value`. It is not clear whether all sources have some implementation of type.
 - Also note that maps keys cannot be type-checked (although their values can).
 
#### Variable compared with variable

Assume previous query, previous assumptions and previous output. Then each path can be type checked as follows : 
	
	type(U1.user.profile.address.number) = number AND
	type(U2.user.profile.address.number) = number AND
	U1.user.profile.address.number = U2.user.profile.address.number AND
	type(U1.user.profile.address.street) = string AND
	type(U2.user.profile.address.street) = string AND 
	U1.user.profile.address.street = U2.user.profile.address.street AND
	type(U1.user.profile.address.apartment) = string AND
	type(U2.user.profile.address.apartment) = string AND 
	U1.user.profile.address.apartment = U2.user.profile.address.apartment AND
	type(U1.user.profile.address.zipcode) = number AND
	type(U2.user.profile.address.zipcode) = number AND 
	U1.user.profile.address.zipcode = U2.user.profile.address.apartment AND
	type(U1.user.profile.address.state) = string AND
	type(U2.user.profile.address.state) = string AND
	U1.user.profile.address.state = U2.user.profile.address.apartment

Notice that arrays and maps cannot be type-checked when comparing two variables (in addition to bags).  

###Path Navigation Rewriter 

 - Assumes type-checking rewriting has already happened.
 - Assumption : consider selection `WHERE A AND B` such that `A` and `B` are predicates. If `A` returns false, we assume `B` will not be evaluated.

#### Variable  compared with a literal
 - A check exists for each navigation path that should evaluate to a scalar or a null.
 - Each path check is placed right before the type check for that navigation path.
 - Map keys and array indices need not be checked individually unless they should evaluate to a tuple. Only the entire map/array needs to be checked. Invalid keys or invalid indices will result in a false, not an error according to SQL++ semantics.
 - Checks are done at every node of the path navigation tree. If a subpath of the currently checked path has not been checked, then an additional check for that subpath is added.  
 - Sample input is the output of the type-check rewriter.
 
Sample Output (fragments):
	
	user != missing AND
	user.profile != missing AND
	user.profile.name != missing AND
	type(user.profile.name) = string AND
	user.profile.name = 'Jules Testard' AND
	...
	user.profile.address != missing AND
	user.profile.address.number != missing AND
	...
	user.profile.phoneNumbers != missing AN
	type(user.profile.phoneNumbers[1]) = number AND
	user.profile.phoneNumbers[1] = 0607588079 AND
	...
	user.profile.hobbies != missing AND
	user.profile.hobbies = {{ {'category' : 'sport','occupation' : 'surfing'} }} AND  
	...
	 
 - Notice that when schema information is available, less navigation checks are required.
 
#### Variables compared with another variable

Assume previous query, previous assumptions and previous output. Then both paths are checked as follows (fragment) :

	...
	U1.user.profile.address != missing AND
	U2.user.profile.address != missing AND
	U1.user.profile.address.number != missing AND
	U2.user.profile.address.number != missing AND
	type(U1.user.profile.address.number) = number AND
	type(U2.user.profile.address.number) = number AND
	U1.user.profile.address.number = U2.user.profile.address.number AND
	...

### Null values Rewriter

 - Assumes path checking has already happened.
 - A null check is added right after each navigation check, unless a null is specifically required by the query.
 - In some systems, null checks might be redundant with type checks. 

#### Variable compared with another literal 

Sample input is the output of the path navigation rewriter.

Sample output (fragment) :  

	user != missing AND
	user != null AND
	user.profile != missing AND
	user.profile != null AND
	user.profile.name != missing AND
	user.profile.name != null AND
	type(user.profile.name) = string AND
	user.profile.name = 'Jules Testard' AND
	...
	user.profile.address != missing AND
	user.profile.address != null AND
	user.profile.address.number != missing AND
	user.profile.address.number != null AND
	...
	user.profile.phoneNumbers != missing AN
	user.profile.phoneNumbers != null AND
	type(user.profile.phoneNumbers[1]) = number AND
	user.profile.phoneNumbers[1] = 0607588079 AND
	...
	user.profile.hobbies != missing AND
	user.profile.hobbies != null AND
	user.profile.hobbies = {{ {'category' : 'sport','occupation' : 'surfing'} }} AND  

## Data source wrappers

### Data source wrapper description

### Example on data sources