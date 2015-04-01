## Polyglot persistence use case : MongoDB and Elastic Search

The blog post for this article is available [here](https://blog.compose.io/mongoosastic-the-power-of-mongodb-and-elasticsearch-together/).

### The Book Database


```
//Mongoose is an object layer which allows MongoDB documents to be 
//accessed as javascript objects.
var mongoose = require("mongoose");

mongoose.connect(process.env.COMPOSE_URL);

var bookSchema = new mongoose.Schema({
  title: String,
  author: String,
  description: String
});'

var Book = mongoose.model("Book", bookSchema);
```

### Mongoosastic

Mongoosastic is a Mongoose plugin which allows using elastic search on top of a MongoDB database. By default, Mongoosastic will replicate the all the fields in a schema into the Elasticsearch database, so by flagging only the fields you want you can reduce duplication. 