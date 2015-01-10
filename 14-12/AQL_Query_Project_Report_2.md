### Asterix vs SQL++ Discrepancies

use dataverse TinySocial;

```
    insert into dataset FacebookUsers ({
       "id":11,
       "alias":"Margarita",
       "name":"MargaritaStoddard",
       "user-since":datetime("2012-08-20T10:10:00"),
       "friend-ids":{{2,3,6,10}},
       "employment":[{
           "organization-name":"Codetechno",
           "start-date":date("2006-08-06")
        }]
    });
    
    for $user in dataset FacebookUsers
    group by $fids := $user.friend-ids  with $user
    return {
     "friends" : $fids,
     "count" : count($fids)
    }
    
    for $user in dataset FacebookUsers
    group by $fids := $user.friend-ids  with $user
    
        
    for $user in dataset FacebookUsers
    group by $e := $user.employment  with $user
    return {
     "friends" : $e,
     "count" : count($e)
    }
```

We identify three types of discrepancies :

 1. operators which exist in SQL++ but are undefined in Asterix (UNION, INTERSECT...).
 - operators which exist in SQL++ which do not exist in AQL but exist "under the covers" in Asterix (LEFT OUTER JOIN...)
 - expressions/functions which have different semantics in SQL++ and AQL and would require a change in Asterix's operators/functions.
 
## Unsupported operators

 - `FULL OUTER JOIN`
 - `UNION [ALL], INTERESECT [ALL], EXCEPT [ALL]`
 - `AT` (positionals variable). However, positional variable argument exists at the logical operator level (for unnest operator). Do not know how it is used.


### 1. Left/Right Outer Join

### 2. Group By Semantics

Out of date in the survey: 

*JSONiq, AQL and BigQuery throws an error when
grouping on complex values (E1, I1, J1)*.

AQL supports grouping of arrays of tuples. However, AQL explicitly forbids comparison of complex values. This is strange.

#### a. with clauses and value unnesting

```
use dataverse TinySocial;
for $user in dataset FacebookUsers
let $a := $user.friend-ids
let $b := count($a)
group by $employment := $user.employment  with $user, $a, $b // grouping by array of tuples
return {
 "employments" : count($employment),
 "a" : count($a),
 "b" : $b
}
```
 



#### b. The SQL++ group variable

###### Primary Key requirements

Data model discrepancy. In AsterixDB clusters, the primary key is also used to hash-partition (a.k.a. shard) the dataset across the nodes of the cluster. What do we do with data coming in which does not follow this requirement?

DDL + insert :

```
drop dataverse Sensors if exists;
create dataverse Sensors;
use dataverse Sensors;

create type CoReadingsType as open {
   reading_id : int32,
   sensor : int32,
   co : double
}

create dataset co_readings(CoReadingsType) primary key reading_id;

insert into dataset co_readings ({
  "reading_id" : 1,
  "sensor" : 1,
  "co" : 0.3
});

insert into dataset co_readings ({
  "reading_id" : 2,
  "sensor" : 1,
  "co" : 0.5  
});

insert into dataset co_readings ({
  "reading_id" : 3,
  "sensor" : 2,
  "co" : 0.6  
});
```

AQL Query :

```
for $c in dataset co_readings
group by $s := $c.sensor with $c
return {
  "sensor" : $s,
  "readings" : for $g in $c return $g.co,
  "number" : count($c),
  "average" : avg(for $g in $c return $g.co)
}
```

SQL++ query :

```
SELECT 	s as sensor,
		( SELECT g.c.co FROM group AS g) AS readings,
		count(group) AS number,
		avg (SELECT g.c.co FROM group AS g) AS average
FROM co_readings AS c
GROUP BY c.sensor AS s
```

Asterix Logical Query Plan :

```
```

### 3. Order by semantics

Error in the survey concerning Asterix. Complex ordering is supported for : 

  - friend-ids
  - tuples
  - arrays of tuples

```
use dataverse TinySocial;

for $user in dataset FacebookUsers
order by $user.employment[0] // tuple
return $user.employment;

for $user in dataset FacebookUsers
order by $user.employment // array of tuples
return $user.employment;

for $user in dataset FacebookUsers
order by $user.friend-ids // bag of ints
return $user.friend-ids;
```

Position (AT) is not supported.


### Complex comparison paradox

```
use dataverse TinySocial;
for $x in dataset FacebookUsers
for $y in dataset FacebookUsers
where $x.friend-ids = $y.friend-ids
return {
  "x" : $x,
  "y" : $y
} // Produces output expected if complex equality supported.

{{1}} = {{1}} // produces an error.
```


### 4. SELECT TUPLE/ELEMENT

```
use dataverse Sensors;

//SELECT ELEMENT c FROM co_readings AS c
for $c in dataset co_readings return $c

//SELECT TUPLE c FROM co_readings AS c
//(implicit order added)
let $c := ( for $r in dataset co_readings return $r)
return $c
```

### 5. Having

```
use dataverse TinySocial;
/**
SELECT user.alias AS alias,
               count(user.friend-ids) AS a,
FROM FacebookUsers AS user
GROUP BY user.alias
HAVING count(user.friend-ids) > 1
*/
for $user in dataset FacebookUsers
let $a := $user.friend-ids
group by $alias := $user.alias  with $user, $a 
where count($a) > 1
return {
  "user" : $alias,
  "a" : count($a)
}
```

### 6. Flatten

```
use dataverse TinySocial;

/**
SELECT user.id AS user_id, friend_ids
FROM INNER FLATTEN (
   FacebookUsers as user,
   user.friend-ids AS friend_ids
)
*/
for $user in dataset FacebookUsers
for $ids in $user.friend-ids
return {
  "user_id" : $user.id,
   "friend_ids" : $ids
}
```

### 7. Syntactic Sugar

```
```
 - `collection comprehensions` (tentative)

#### Notes 

 - Complex grouping is supported!
 - show limitations of groupby count. no field acccesses within the $user if in with clause.
 -  the group symbol in SQL++ is not present in asterix.
 - distinct by