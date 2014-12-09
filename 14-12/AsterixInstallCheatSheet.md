## Asterix command line cheat sheet

 - [How to import asterix to Eclipse](https://code.google.com/p/asterixdb/wiki/ImportingAsterixIntoEclipse)
 - [Maven skip tests](http://maven.apache.org/surefire/maven-surefire-plugin/examples/skipping-test.html)
 - To build a release, just do `mvn install -Dskiptests`. You will find the executable here : `asterixdb/asterix-installer/target/asterix-installer-0.8.7-SNAPSHOT-binary-assembly.zip`.
 - Test SQLPP : run junit tests from eclipse.


Running tests :
If you encounter any problems running tests in the asterix-app project, ensure first that all other project have built and installed successfully.

 - `mvn -Dmaven.test.skip=true install` this installs without compiling tests
 - `mvn install -DSkipTests` this installs without running tests.