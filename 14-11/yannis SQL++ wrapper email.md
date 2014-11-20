Hello Yannis and Kian Win,

I am sending you this email because I believe that a SQL++ wrapper for AsterixDB is not a good idea, and I have several reasons to believe so :

##### 1.  Asterix is not Forward

We want to install a SQL++ interface on top of Asterix which is not nearly as powerful as Forward :

   - SQL++ is meant for multiple sources, while we will always query AsterixDB on this wrapper.
   - The SQL++ contains constructs that do not exist in AsterixDB
   - The Asterix Data Model is not the SQL++ data model

In other words, we will have a large number of valid SQL++ queries that would be invalid on that interface, which would be at the very best awkward, at worst terribly misleading.

##### 2. Asterix does not have a SQL++ parser

If we setup a SQL++ interface on a Asterix client, we will need at the very least to import our own parser and plan translator, which adds a useless overhead given the query was already parsed when submitted to forward in the first place. If we want this interface to be stand alone (i.e. used in a context other than forward), then we will need to include our plan optimizer as well, which adds even more code to the Asterix codebase (which they will have to maintain and so on). We will also probably need to do tweaks to these components to make sure the parser doesn't try to interpret plans valid on Forward but invalid on Asterix. 

I don't believe it is feasible to ask the Asterix guys to maintain half of our query compiler's code base just to let us send queries to Asterix.

##### 3. We will incur unnecssary overhead

Given the query plan obtained from the Forward distributor, we would have to tranlsate that plan back to some SQL++ string and then parse that string into a plan again, when we could have sent the plan to Asterix almost "as is" in the first place.


##### 4. We can't expect every data source we support to support SQL++ directly

While the Asterix guys are kind enough to let us add a SQL++ wrapper on top of their software, that won't be the case for every new data source we support, especially industry/closed source data sources. We will need to find a new model of source integration in the future.

-------------

Fortunately, there are preferable alternatives.

##### 1. Algebricks Logical Plan Interface:

I have looked at the Asterix Code base, and identified the Algebricks class which most closely resembles our definition of a logical plan, and they are quite similar. I am quite confident that we can eventually write a Algebricks Job Interface, which is the one which most closely resembles our distributors output.

There is one problem which we already identified, which is the lack of an explicit normal form for that plan. I haven't asked formally the AsterixDB guys what their normal form is yet, because I wanted to fix the direction in which we are going first.

I believe I can find one of their guys who is knowledgeable on the Algebricks compiler to help me with the normal form and the interface.

##### 2. Stick with the AQL interface:

I know we had previously ruled out this option, but I wished to bring it up again for a particular reason. We are particularily lucky that the AsterixDB team is willing to make so much effort to accomodate our needs for the Forward interface. I believe we won't be so lucky with the next datasources we wish to support, especially if they originate from the industry/closed source community. 


AQL provides a normal form in the form its language specification. We can use it as our basis to build Asterix-compliant plans. Even then, we can still use the knowledge of the Algebricks normal form to understand how the AQL compiler will generate plans for improvement.


#### Conclusion 

My opinion would be to go with option 2, given this allows us to consider Asterix as a black box and still be able to achieve all the goals set for the Forward query compiler. Finally, this will also allows up to use the same integration model with our next data source.