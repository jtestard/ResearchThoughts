If we go back to issue #854 (https://code.google.com/p/asterixdb/issues/detail?id=854), which talks purely about AQL,

We would want to rewrite something like :

```
let $xs := {{
    { "id" : 1, "age" :  12 },
   { "age" : 12, "id" : 1}
}}
for $x in $xs
distinct by $x.id, $x.age
return $x
```


Into something like :


```
let $xs := {{
    { "id" : 1, "age" :  12 },
   { "age" : 12, "id" : 1}
}}
for $x in $xs
group by $id := $x.id, $age := $x.age with $x
return { "id" : $id, "age" : $age }
```