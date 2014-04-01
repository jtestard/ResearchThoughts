WITH Seniors AS (SELECT * FROM "People" WHERE age > 49),
SeniorsTwo AS (SELECT * FROM "PeopleTwo" WHERE age > 49)
SELECT Seniors.name as "Person1" , SeniorsTwo.name as "Person2", Seniors.country
FROM Seniors, SeniorsTwo
WHERE (Seniors.country = SeniorsTwo.country)
LIMIT 10;