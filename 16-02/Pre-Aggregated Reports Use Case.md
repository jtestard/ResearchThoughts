Hi Yannis and Vicky,

In this email I am giving a possible non-synthetic running example and suggest a way to include this example in the paper.

### Running Example

This case is a MongoDB use case found [here](https://docs.mongodb.org/ecosystem/use-cases/pre-aggregated-reports/).

The idea is to take an event collections (for web pages in web servers) with the following schema:

```
event(day, hour, minute, site, page)
```

And the goal is to transform this collection into the following:

```
{
    _id: ...,
    metadata: {
        day: ISODate("2000-10-10"),
        site: "site-1",
        page: "/apache_pb.gif" },
    daily: 5468426,
    hourly: [
        {"hour":0, "hit":227850},
        {"hour":1, "hit":210231},
        ...
        {"hour":23, "hit":20457}]
    minute: [
        {"minute":0, "hit":2332},
        {"minute":1, "hit":7291},
        ...
        {"minute":1439, "hit":3102}]
},
...
```

Where each document pre-aggregates the daily, hourly and minutely hit counts for a given web page on a given day.

The MongoDB use case described online accomplishes this by transforming each tuple individually as it is inserted into the system. This is because MongoDB **does not** have the capability to project nested collections.

The entire transformation can however be written using the following SQL++ query:

SQL++ Query using the group variable:

```
SELECT
	{'day':e.day, 'site' : e.site, 'page' : e.page} AS metadata, 
	COUNT(*) AS daily,
	( SELECT g.hour AS hour, COUNT(*) AS hit
	  FROM group AS g
	  GROUP BY g.hour
	) AS hourly,
	( SELECT g.hour * 60 + g.minute AS minute, COUNT(*) AS hit
	  FROM group AS g
	  GROUP BY g.hour, g.minute
	) AS minute
FROM events AS e
GROUP BY e.day, e.site, e.page
```

SQL++ Query without the group variable:

```
SELECT
	{'day':e.day, 'site' : e.site, 'page' : e.page} AS metadata, 
	COUNT(*) AS daily,
	( SELECT f.hour AS hour, COUNT(*) AS hit
	  FROM events AS f
	  WHERE e.day=f.day AND e.site=f.site AND e.page=f.page
	  GROUP BY f.hour
	) AS hourly,
	( SELECT f.hour * 60 + f.minute AS minute, COUNT(*) AS hit
	  FROM events AS f
	  WHERE e.day=f.day AND e.site=f.site AND e.page=f.page
	  GROUP BY f.hour, f.minute
	) AS minute
FROM events AS e
GROUP BY e.day, e.site, e.page
```

### Supported Databases 

On page 19 of the SQL++ Survey of NoSQL languages is shown a chart of the query languages which support nested collections in the select clause:

 - Jaql
 - JSONiq
 - AQL

Databases for each query language:

 - AQL: AsterixDB (Semi-structured Database)
 - JSONiq: IBM WebSphere (Data Integration Middleware), Zorba
 - Jaql: IBM BigInsights InfoSphere (powered by Hadoop)

So it is clear that we really need our running example to be supported by a "real-world” use case (artificial TPC-H like query is not enough).