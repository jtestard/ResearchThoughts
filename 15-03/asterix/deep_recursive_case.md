### Deep recursive case

```
use dataverse TinySocial;

from FacebookUsers as user
left outer join (
  select user-inner.id as id,
               user-inner.name as name,
               message.message as message
  from FacebookUsers as user-inner
  left outer join
  FacebookMessages as message
  on user-inner.id = message.author-id
) as inner-result
on user.id = inner-result.id
select user.name as outer-name, inner-result as result;
```