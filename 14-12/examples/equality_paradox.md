## Equality "Paradox"

According to the v4 version of the [SQL++ survey](http://arxiv.org/pdf/1405.3631v4.pdf), complex equality results in an error in AQL. This is consistent with the second example, but not the first.

Query with DDL and data :

```
drop dataverse Sensors if exists;
create dataverse Sensors;
use dataverse Sensors;

create type CoReadingsType as open {
   reading_id : int32,
   sensor : int32,
   co : [double]
}

create dataset co_readings(CoReadingsType) primary key reading_id;

insert into dataset co_readings ({
  "reading_id" : 1,
  "sensor" : 1,
  "co" : [0.3]
});

insert into dataset co_readings ({
  "reading_id" : 2,
  "sensor" : 1,
  "co" : [0.5, 0.7]
});

insert into dataset co_readings ({
  "reading_id" : 3,
  "sensor" : 2,
  "co" : [0.5, 0.7]
});

for $x in dataset co_readings
for $y in dataset co_readings
where $x.co = $y.co
return {
  "x" : $x,
  "y" : $y
} // Produces output expected if complex equality supported.

{{1}} = {{1}} // produces an error.
```

### Results

First query result :

```
{ "x": { "reading_id": 1, "sensor": 1, "co": [ 0.3d ] }, "y": { "reading_id": 1, "sensor": 1, "co": [ 0.3d ] } }
{ "x": { "reading_id": 2, "sensor": 1, "co": [ 0.5d ] }, "y": { "reading_id": 2, "sensor": 1, "co": [ 0.5d ] } }
{ "x": { "reading_id": 2, "sensor": 1, "co": [ 0.5d ] }, "y": { "reading_id": 3, "sensor": 2, "co": [ 0.5d ] } }
{ "x": { "reading_id": 3, "sensor": 2, "co": [ 0.5d ] }, "y": { "reading_id": 2, "sensor": 1, "co": [ 0.5d ] } }
{ "x": { "reading_id": 3, "sensor": 2, "co": [ 0.5d ] }, "y": { "reading_id": 3, "sensor": 2, "co": [ 0.5d ] } }
```

Second query result :

```
Comparison for UNORDEREDLIST is not supported. [AlgebricksException]
```