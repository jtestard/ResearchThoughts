This document narrates some of the issues I struggled with while installing and running different components of the Forward codebase.

## Trac Wiki 
It is not really clear when looking at the project documentation what are the roles of different projects and how they relate to each other (code/config inspection was required to come up with an interpretation).

##1
problems with ONLINE IDE documentation : seems like 
/Users/julestestard/Projects/svn/forward/trunk/src/ide/src/main/resources/edu/ucsd/forward/ide/data
does not contain the metadata sql files any more. However they were found in test/java/resources/edu/ucsd/forward/ide/data/metadata.backup

##2
workspc_loc is outdated (should refer to query compiler instead of sketch). **Modified accordingly in the AsterixDB branch.**

##3
When attempting to run the IDE project, the data program found was `ide-data-source.xml`
Configs of the IDE project : 

Instruction on postgres should stipulate expected settings (development):
	
	port : 5432
	user : postgres
	pswd : postgres
	database : forward

##4
Maven build before start project :) [otherwise one gets messages with import problems].
I have attempted to run the Website eclipse configuration (on the Website project) (and have been careful to run with java 1.6) and have run into this error :

	Exception in thread "main" java.lang.Error: Unresolved compilation problems: 
	Application cannot be resolved to a type
	IdeBuilder cannot be resolved to a type
	The method build() from the type Main refers to the missing type Application
	IdeBuilder cannot be resolved to a type
	ApplicationBuildingException cannot be resolved to a type
	Logger cannot be resolved to a type
	ApplicationBuildingResult cannot be resolved to a type
	CheckedException cannot be resolved to a type
	Logger cannot be resolved to a type
	Application cannot be resolved to a type
	Config cannot be resolved
	Config cannot be resolved
	Config cannot be resolved
	Config cannot be resolved
	ApplicationServer cannot be resolved to a type
	ApplicationServer cannot be resolved to a type
	ApplicationServer cannot be resolved
	ApplicationException cannot be resolved to a type
	Logger cannot be resolved to a type

	at edu.ucsd.forward.website.Main.main(Main.java:405)


##5
Followed instructions (given caveat 1), but got this error.

	Query path "username" is ambiguous. Matches were found in the following scopes: SQL++ query context, FPL context. file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/ide/target/classes/edu/ucsd/forward/ide/function/security/invite_user.sql (56:29-56:36)
	edu.ucsd.forward.query.QueryCompilationException: Query path "username" is ambiguous. Matches were found in the following scopes: SQL++ query context, FPL context.
	
##6
Further problems compiling the website project (website eclipse configuration). Server seems to start, but getting 404 error when connecting to `http://localhost:8080/`.

Getting this error message on : 
	
	2014-10-28 22:31:51,813 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED o.e.j.w.WebAppContext{,file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/website/}: java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser
	2014-10-28 22:31:51,819 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED o.e.j.w.WebAppContext{/ide,file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/website/}: java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser
	2014-10-28 22:31:51,820 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED org.eclipse.jetty.server.handler.ContextHandlerCollection@719cec59: MultiException[java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser, java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser]
	2014-10-28 22:31:51,820 WARN  org.eclipse.jetty.server.Server.(Server.java:257) - Error starting handlers
	org.eclipse.jetty.util.MultiException: Multiple exceptions
	at org.eclipse.jetty.server.handler.HandlerCollection.doStart(HandlerCollection.java:186)
	at 	org.eclipse.jetty.server.handler.ContextHandlerCollection.doStart(ContextHandlerCollection.java:164)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:58)
	at org.eclipse.jetty.server.handler.HandlerWrapper.doStart(HandlerWrapper.java:93)
	at org.eclipse.jetty.server.Server.doStart(Server.java:253)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:58)
	at edu.ucsd.forward.server.JettyServer.start(JettyServer.java:169)
	at edu.ucsd.forward.server.ApplicationServer.start(ApplicationServer.java:154)
	at edu.ucsd.forward.website.Main.main(Main.java:455)

##7
JSTestDriver 

    Exception in thread "main" com.google.jstestdriver.config.ConfigurationException: Unable to read configuration file.
    	at com.google.jstestdriver.config.UserConfigurationSource.parse(UserConfigurationSource.java:57)
    	at com.google.jstestdriver.embedded.JsTestDriverBuilder.setConfigurationSource(JsTestDriverBuilder.java:258)
    	at com.google.jstestdriver.embedded.JsTestDriverBuilder.setDefaultConfiguration(JsTestDriverBuilder.java:95)
    	at edu.ucsd.forward.JsTestDriverServer.defaultBuilder(JsTestDriverServer.java:120)
    	at edu.ucsd.forward.JsTestDriverServer.getInstance(JsTestDriverServer.java:94)
    	at edu.ucsd.forward.JsTestDriverRunner.<init>(JsTestDriverRunner.java:72)
    	at edu.ucsd.forward.JsTestDriverRunner.<init>(JsTestDriverRunner.java:59)
    	at edu.ucsd.forward.JsTestDriverRunner.main(JsTestDriverRunner.java:434)
    Caused by: java.io.FileNotFoundException: /Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/units\jsTestDriver.conf (No such file or directory)
    	at java.io.FileInputStream.open(Native Method)
    	at java.io.FileInputStream.<init>(FileInputStream.java:120)
    	at com.google.jstestdriver.config.UserConfigurationSource.parse(UserConfigurationSource.java:53)
    	... 7 more
