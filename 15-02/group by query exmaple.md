```
use dataverse TinySocial;

for $fb in dataset FacebookUsers
for $fm in dataset FacebookMessages
where $fb.id = $fm.author-id
let $group := { "fb" : $fb, "fm" : $fm }
group by $loc := $fm.sender-location with $group
where $loc = point("34.45,96.48")
return {
  "results" : for $g in $group
              return $g.fb.name
};
```

```
use dataverse TinySocial;

from FacebookUsers as fb
join FacebookMessages as fm
on fb.id = fm."author-id"
group by fm."sender-location" as loc
having loc = point("34.45,96.48")
select element {
   "results" : (from group as g
               select element g.fb.name)
};
```