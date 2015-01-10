### Complex grouping and ordering

According to the v4 version of the [SQL++ survey](http://arxiv.org/pdf/1405.3631v4.pdf), complex ordering and complex grouping said to result in an error in AQL. From these examples, it would seem that this is not the case.

```
drop dataverse TinySocial2 if exists;
create dataverse TinySocial2;
use dataverse TinySocial2;

    create type EmploymentType as open {
        organization-name: string,
        start-date: date,
        end-date: date?
    }

    create type FacebookUserType as closed {
        id: int32,
        alias: string,
        name: string,
        user-since: datetime,
        friend-ids: {{ int32 }},
        employment: [EmploymentType]
    }

    create dataset FacebookUsers(FacebookUserType)
    primary key id;

insert into dataset FacebookUsers(
    {"id":1,"alias":"Margarita","name":"MargaritaStoddard","user-since":datetime("2012-08-20T10:10:00"),"friend-ids":{{2,3,6,10}},"employment":[{"organization-name":"Codetechno","start-date":date("2006-08-06")}]}
);

insert into dataset FacebookUsers(
    {"id":2,"alias":"Isbel","name":"IsbelDull","user-since":datetime("2011-01-22T10:10:00"),"friend-ids":{{1,4}},"employment":[{"organization-name":"Hexviafind","start-date":date("2010-04-27")}]}
);

insert into dataset FacebookUsers(
    {"id":3,"alias":"Emory","name":"EmoryUnk","user-since":datetime("2012-07-10T10:10:00"),"friend-ids":{{1,5,8,9}},"employment":[{"organization-name":"geomedia","start-date":date("2010-06-17"),"end-date":date("2010-01-26")}]});

insert into dataset FacebookUsers(
    {"id":4,"alias":"Emory","name":"EmoryUnk","user-since":datetime("2012-07-10T10:10:00"),"friend-ids":{{1,5,8,9}},"employment":[{"organization-name":"geomedia","start-date":date("2010-06-17"),"end-date":date("2010-01-26")}]});

//Query 1
for $user in dataset FacebookUsers
let $a := $user.friend-ids
let $b := count($a)
group by $employment := $user.employment  with $user, $a, $b // grouping by array of tuples
return {
 "employments" : $employment,
 "a" : count($a),
 "b" : $b
}

//Query 2
for $user in dataset FacebookUsers
order by $user.employment 
return $user

//Query 3
for $user in dataset FacebookUsers
order by $user.friend-ids 
return $user
```


### Results

#### Query 1

```
{ "employments": [ { "organization-name": "Codetechno", "start-date": date("2006-08-06"), "end-date": null } ], "a": 1i64, "b": [ 4i64 ] }
{ "employments": [ { "organization-name": "Hexviafind", "start-date": date("2010-04-27"), "end-date": null } ], "a": 1i64, "b": [ 2i64 ] }
{ "employments": [ { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } ], "a": 2i64, "b": [ 4i64, 4i64 ] }
```

#### Query 2

```
{ "id": 1, "alias": "Margarita", "name": "MargaritaStoddard", "user-since": datetime("2012-08-20T10:10:00.000Z"), "friend-ids": {{ 2, 3, 6, 10 }}, "employment": [ { "organization-name": "Codetechno", "start-date": date("2006-08-06"), "end-date": null } ] }
{ "id": 2, "alias": "Isbel", "name": "IsbelDull", "user-since": datetime("2011-01-22T10:10:00.000Z"), "friend-ids": {{ 1, 4 }}, "employment": [ { "organization-name": "Hexviafind", "start-date": date("2010-04-27"), "end-date": null } ] }
{ "id": 3, "alias": "Emory", "name": "EmoryUnk", "user-since": datetime("2012-07-10T10:10:00.000Z"), "friend-ids": {{ 1, 5, 8, 9 }}, "employment": [ { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } ] }
{ "id": 4, "alias": "Emory", "name": "EmoryUnk", "user-since": datetime("2012-07-10T10:10:00.000Z"), "friend-ids": {{ 1, 5, 8, 9 }}, "employment": [ { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } ] }
```

#### Query 3

```
{ "id": 2, "alias": "Isbel", "name": "IsbelDull", "user-since": datetime("2011-01-22T10:10:00.000Z"), "friend-ids": {{ 1, 4 }}, "employment": [ { "organization-name": "Hexviafind", "start-date": date("2010-04-27"), "end-date": null } ] }
{ "id": 3, "alias": "Emory", "name": "EmoryUnk", "user-since": datetime("2012-07-10T10:10:00.000Z"), "friend-ids": {{ 1, 5, 8, 9 }}, "employment": [ { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } ] }
{ "id": 4, "alias": "Emory", "name": "EmoryUnk", "user-since": datetime("2012-07-10T10:10:00.000Z"), "friend-ids": {{ 1, 5, 8, 9 }}, "employment": [ { "organization-name": "geomedia", "start-date": date("2010-06-17"), "end-date": date("2010-01-26") } ] }
{ "id": 1, "alias": "Margarita", "name": "MargaritaStoddard", "user-since": datetime("2012-08-20T10:10:00.000Z"), "friend-ids": {{ 2, 3, 6, 10 }}, "employment": [ { "organization-name": "Codetechno", "start-date": date("2006-08-06"), "end-date": null } ] }
```


