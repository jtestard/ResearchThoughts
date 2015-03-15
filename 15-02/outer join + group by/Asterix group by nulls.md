SQL++ 

```
from {{
    {"id" : 1, "name" : "alice", "employer" : "McDonald's" },
    {"id" : 2, "name" : "bob", "employer" : "unknown" },
    {"id" : 3, "name" : "chad", "employer" : null },
    {"id" : 4, "name" : "david" },
    {"id" : 5, "name" : "esther", "employer" : "McDonald's" }
}} as person
group by person.employer as employer
select employer as employer, group as group
```


AQL 

```
let $x := {{
    {"id" : 1, "name" : "alice", "employer" : "McDonald's" },
    {"id" : 2, "name" : "bob", "employer" : "unknown" },
    {"id" : 3, "name" : "chad", "employer" : null },
    {"id" : 4, "name" : "david" },
    {"id" : 5, "name" : "esther", "employer" : "McDonald's" }
}}
for $person in $x
let $group := { "person" : $person }
group by $employer := $person.employer with $group
return {
  "employer" : $employer,
  "group" : $group
};
```


Possible bug :

```
let $x := {{
    {{ 1, 2 }}, {{ "a", "b" }} , {{ "b" , "a" }} 
}}
for $person in $x
let $group := { "person" : $person }
group by $person := $person with $group
return {
  "person" : $person,
  "group" : $group
};
```


```
{ "group": [ { "person": {{ "a", "b" }} } ], "person": {{ "a", "b" }} }
{ "group": [ { "person": {{ "b", "a" }} } ], "person": {{ "b", "a" }} }
{ "group": [ { "person": {{ 1, 2 }} } ], "person": {{ 1, 2 }} }
```

Other bug : 

```
let $x := {{
    { "id" : 1, "age" :  12 },
   { "age" : 12, "id" : 1}
}}
for $person in $x
let $group := { "person" : $person }
group by $person := $person with $group
return {
  "person" : $person,
  "group" : $group
};
```

```
{ "person": { "id": 1, "age": 12 }, "group": [ { "person": { "id": 1, "age": 12 } } ] }
{ "person": { "age": 12, "id": 1 }, "group": [ { "person": { "age": 12, "id": 1 } } ] }
```