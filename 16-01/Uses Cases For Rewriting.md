# Use Cases for Rewriting

 - Analytics Website built with MongoDB, CouchDB
 - Informatica Workflow with a relational database and Hadoop
 - AsterixDB Analytics Use Cases
 - TPC-BB

### What we need to do:

 - Relate use cases to the rewritings.
 - Why do I want this => People care about this query

## Scenarios

### Analytics Website

Question: what are the query requirements of websites displaying visualizations

What kind of queries are requested? What do they looking like?

Expectations:

 - Data to be visualized is relatively small, to be displayed on a screen.
 - Data from which the visualization is taken may be much larger, typicaly a relational or NoSQL database.

In Costas's work, updates are received in the form of flat tuples.

### Informatica Workflow

Look at talks about Informatica + Hadoop use cases.

### AsterixDB Analytics Use Case

Find 


The rewriting is compelling when nesting is desired in the output. When is it the case?

### Online APIs

REST APIs :

 - Keen IO: has group by which exhibits nesting [link](https://keen.io/docs/api/?javascript#group-by)
 - Algolia : [link](https://www.algolia.com/doc/ruby#query-json-answer)

Rest API calls: typically simple 

Keen IO:

**Query**

```
var count = new Keen.Query("count", {
  eventCollection: "user_logins",
  group_by: "user.email",
  timeframe: "previous_3_days",
  interval: "daily"
});
```

**Results**

```
{
  "result": [
    {
      "timeframe": {
        "start": "2014-08-22T00:00:00.000Z",
        "end": "2014-08-23T00:00:00.000Z"
      },
      "value": [
        {
          "user.email": "ryan@keen.io",
          "result": 3
        },
        {
          "user.email": "dan@keen.io",
          "result": 2
        },
        {
          "user.email": "kirk@keen.io",
          "result": 1
        }
      ]
    },
    {
      "timeframe": {
        "start": "2014-08-23T00:00:00.000Z",
        "end": "2014-08-24T00:00:00.000Z"
      },
      "value": [
        {
          "user.email": "ryan@keen.io",
          "result": 0
        },
        {
          "user.email": "dan@keen.io",
          "result": 1
        },
        {
          "user.email": "kirk@keen.io",
          "result": 1
        }
      ]
    },
    {
      "timeframe": {
        "start": "2014-08-25T00:00:00.000Z",
        "end": "2014-08-26T00:00:00.000Z"
      },
      "value": [
        {
          "user.email": "ryan@keen.io",
          "result": 5
        },
        {
          "user.email": "dan@keen.io",
          "result": 4
        },
        {
          "user.email": "kirk@keen.io",
          "result": 0
        }
      ]
    }
  ]
}
```