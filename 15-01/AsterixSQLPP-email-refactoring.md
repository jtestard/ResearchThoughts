Hello all,

I wanted to send this email to give a little status update. I have managed to get two features working this week :

 - A SQL++ Parser built with JAVACC which parses simple SelectFromWhere queries and AQL “use dataverse” statements (feature currently on code review).
 - The refactoring of the Asterix framework discussed last week (ready to be reviewed, available on Asterix sandbox).

My plan is to add this afternoon/tonight a simple interface based on the Asterix front end web interface to see both features in action. I was wondering if we should schedule a Skype (or in person) meeting tomorrow morning before (or after) the AsterixDB all-hands to discuss.

Jules

Hello Ian,

I am looking for a guide on how to deploy Asterix when I am working on it. I have looked at the [wikis on the website](https://code.google.com/p/asterixdb/w/list), but did not find any guide.

Here is what I came up with so far : 

1) I know how to build and install using Maven :

	cd $ASTERIX_ROOT
	mvn install -DskipTests
	mvn test -Dtest=<Test-Suite-Name>

where `$ASTERIX_ROOT` is the top-level folder of the Asterix project. 

2) The Maven installation will create a `asterix-installer-0.8.7-SNAPSHOT-binary-assembly.zip` file in the `asterix-installer` module. I can then try follow the [website installation guide](https://asterixdb.ics.uci.edu/documentation/install.html) to create and start a new AsterixDB instance.

This sounds a little ad-hoc. Is there a better solution?

Best,

Jules Testard