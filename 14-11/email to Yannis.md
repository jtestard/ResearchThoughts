Ok,

I have talked with Kian Win this morning and I think there was some confusion indeed.

I believed that the primary purpose of the SQL++ interface on top of Asterix was to serve SQL++ queries produced by the Forward query processor’s Asterix wrapper, in the sense that both the AsterixDB wrapper in Forward and the SQL++ interface in Asterix would be part of the same goal/project. 

In that context, a SQL++ interface on top of Asterix did not make as much sense given a Algebricks job or AQL interface could have done the same job in a much simpler way. Now given that the two projects are separate, this changes the situation to some extent, but:

 - The point **1.** from the previous email still remains. I guess we will have to be careful about how we go about this "Asterix-supported" SQL++ subset.
 - The point **3.** from the previous email also still remains. If we use a SQL++ interface to send plans from Forward to Asterix, we incur the cost and the work of building a AsterixDB wrapper (on Forward) which has to translate a source-annotated query plan back into a SQL++ query, which then has  to be processed again by the SQL++ wrapper on the Asterix side.

In this situation, I believe the best approach is to first build an Algebricks Job interface (Algebricks jobs look like logical query plans), which is currenlty non-existent on the Asterix side, as far as I know. Once this interface is done, we can :

 - Build the SQL++ interface on Asterix by translating SQL++ queries into Algebricks jobs.
 - Have the Asterix wrapper on the Forward query processor send Algebricks jobs instead of SQL++ queries.
 
This requires knowledge of the Algebricks job normal form, which I haven't got from the Asterix guys yet, but I am working on it and will get it as soon as possible.

PS: on a last note, I am not so confident we will have access to such normal forms for all the data sources which we eventually want to support. Is there an alternative model for source integration?

Sorry for the previous blank message,

Jules

