Hello,

My name is Jules Testard and I am a Ph.D. student from UCSD working with Yannis Papakonstantinou.

I am currently writing an AsterixDB interface for the SQL++ Forward Query Processor currenlty in the works at UCSD : http://forward.ucsd.edu/.

I would wish to join this google group in order to : 
 - Provide feedback about my interactions with AsterixDB.
 - Get help with set up or usage issues I may be faced with while using AsterixDB.

Thank very much for your consideration,

Best,

Jules Testard
Ph.D. Student
University of California, San Diego
9500 Gilman Drive
92037, California, USA
Tel : (+1) 858-997-9311

===============================

Here is described a (hopefully simple) issue I was hoping to get help with :

I am currently trying to install AsterixDB on Mac OS X 10.9. I am following the guide described here : https://asterixdb.ics.uci.edu/documentation/install

I have successfully followed the steps of section 1 until I arrived to the `managix create -n my_asterix -c $MANAGIX_HOME/clusters/local/local.xml` command. When I execute this command I get the following output : 

	[julestestard@MacBook-Air-de-Jules-2 managix]$ managix create -n my_asterix -c $MANAGIX_HOME/clusters/local/local.xml
	ERROR: Unable to start Zookeeper Service. This could be because of the following reasons.
	1) Managix is incorrectly configured. Please run managix validate to run a validation test and correct the errors reported.
	2) If validation in (1) is successful, ensure that java_home parameter is set correctly in Managix configuration (conf/managix-conf.xml)

Here is the context of the error :

I am using : 

 - `JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home`
 - I am using Java version 1.7.0_67

My `managix validate` command output looks fine : 

	[julestestard@MacBook-Air-de-Jules-2 managix]$ managix validate
	INFO: Environment [OK]
	INFO: Managix Configuration [OK]

The only explanation I can think of is if zookeeper is missing and must be downloaded seperately. Is this the case (the installation guide does not talk about it)?