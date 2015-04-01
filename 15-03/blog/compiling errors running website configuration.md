Error : seems an expected class cannot be found : org.eclipse.jetty.xml.XmlParser.

I added an extra jar to the build path : things crashed and now jars are missing.

How do I regenerate jars?

Error I am getting when runnign website configuration :

```
Exception in thread "main" java.lang.NoClassDefFoundError: edu/ucsd/forward/application/ApplicationBuildingException
Caused by: java.lang.ClassNotFoundException: edu.ucsd.forward.application.ApplicationBuildingException
	at java.net.URLClassLoader$1.run(URLClassLoader.java:202)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.net.URLClassLoader.findClass(URLClassLoader.java:190)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:306)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:301)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:247)
```

Errors I am getting using mvn install :

```
mvn install
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building FORWARD Website 0.9.1-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[WARNING] The POM for edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT is missing, no dependency information available
[WARNING] The POM for edu.ucsd.forward:sqlpp-ri:jar:0.9.1-SNAPSHOT is missing, no dependency information available
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 0.345 s
[INFO] Finished at: 2015-03-12T16:54:44-07:00
[INFO] Final Memory: 7M/156M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal on project website: Could not resolve dependencies for project edu.ucsd.forward:website:jar:0.9.1-SNAPSHOT: The following artifacts could not be resolved: edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT, edu.ucsd.forward:sqlpp-ri:jar:0.9.1-SNAPSHOT: Failure to find edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT in http://maven.forward.ucsd.edu was cached in the local repository, resolution will not be reattempted until the update interval of forward.ucsd.edu has elapsed or updates are forced -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/DependencyResolutionException
```

Simply seems that there are missing maven dependencies. 

```
mvn package
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building FORWARD Website 0.9.1-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[WARNING] The POM for edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT is missing, no dependency information available
[WARNING] The POM for edu.ucsd.forward:sqlpp-ri:jar:0.9.1-SNAPSHOT is missing, no dependency information available
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 0.419 s
[INFO] Finished at: 2015-03-12T17:18:31-07:00
[INFO] Final Memory: 6M/123M
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal on project website: Could not resolve dependencies for project edu.ucsd.forward:website:jar:0.9.1-SNAPSHOT: The following artifacts could not be resolved: edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT, edu.ucsd.forward:sqlpp-ri:jar:0.9.1-SNAPSHOT: Failure to find edu.ucsd.forward:ide:jar:0.9.1-SNAPSHOT in http://maven.forward.ucsd.edu was cached in the local repository, resolution will not be reattempted until the update interval of forward.ucsd.edu has elapsed or updates are forced -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/DependencyResolutionException
```