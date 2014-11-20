This document narrates some of the issues I struggled with while installing and running different components of the Forward codebase. Issues that have been fixed and/or not fixed are described here.

### Documents Modified 

 - https://trac.forward.ucsd.edu/main/wiki/Development/Postgresql
 - https://trac.forward.ucsd.edu/main/wiki/Development/Running
 - https://trac.forward.ucsd.edu/main/wiki/Development/Running-Applications

###1
It is not really clear when looking at the project documentation what are the roles of different projects and how they relate to each other (code/config inspection was required to come up with an interpretation). **TODO** : make the documentation of the interactions between the different projects more explicit.

###2
problems with ONLINE IDE documentation : seems like 
/Users/julestestard/Projects/svn/forward/trunk/src/ide/src/main/resources/edu/ucsd/forward/ide/data
does not contain the metadata sql files any more. However they were found in test/java/resources/edu/ucsd/forward/ide/data/metadata.backup

**Comments added** in the Running Test Cases and/or Applications document.

###3
PostgreSQL expected settings made explicit in the install docs.

###4
In the IDE eclipse project configuration, under Arguments > Program Arguments : workspc_loc is outdated (should refer to query compiler instead of sketch since the rename of the project). **Modified accordingly in the AsterixDB branch.**

###5
Maven build before start project :) [otherwise one gets messages with compilation problems].

###6
I have attempted to run the Website eclipse configuration and have run into this error :

	2014-10-29 14:10:08,840 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED o.e.j.w.WebAppContext{,file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/website/}: java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser
	2014-10-29 14:10:08,844 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED o.e.j.w.WebAppContext{/ide,file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/website/}: java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser
	2014-10-29 14:10:08,845 WARN  org.eclipse.jetty.util.component.AbstractLifeCycle.(AbstractLifeCycle.java:196) - FAILED org.eclipse.jetty.server.handler.ContextHandlerCollection@36fcd774: MultiException[java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser, java.lang.NoClassDefFoundError: org/eclipse/jetty/xml/XmlParser]
	2014-10-29 14:10:08,845 WARN  org.eclipse.jetty.server.Server.(Server.java:257) - Error starting handlers
	org.eclipse.jetty.util.MultiException: Multiple exceptions
		at org.eclipse.jetty.server.handler.HandlerCollection.doStart(HandlerCollection.java:186)
		at org.eclipse.jetty.server.handler.ContextHandlerCollection.doStart(ContextHandlerCollection.java:164)
		at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:58)
		at org.eclipse.jetty.server.handler.HandlerWrapper.doStart(HandlerWrapper.java:93)
		at org.eclipse.jetty.server.Server.doStart(Server.java:253)
		at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:58)
		at edu.ucsd.forward.server.JettyServer.start(JettyServer.java:169)
		at edu.ucsd.forward.server.ApplicationServer.start(ApplicationServer.java:154)
		at edu.ucsd.forward.website.Main.main(Main.java:455)
		2014-10-29 14:10:08,883 INFO  org.eclipse.jetty.server.AbstractConnector.		(AbstractConnector.java:324) - Started SelectChannelConnector@0.0.0.0:8080 STARTING

NOTE : Server seems to start, but getting 404 error when connecting to `http://localhost:8080/`.

Troubleshooting done : 

 - I have verified all databases have been created and populated correctly according to descriptions found in documentation.
 - I have verfied Java version (1.6) and PostgreSQL version (9.1).

###7
I have attempted to run the IDE eclipse configuration and have run into this error :

    2014-10-29 14:55:54,083 ERROR edu.ucsd.forward.data.source.AbstractDataSource.(AbstractDataSource.java:105) - Encountered active transactions when closing data source: fpl_local_scope
    2014-10-29 14:55:54,090 ERROR edu.ucsd.forward.ide.Main.(Main.java:182) - Query path "username" is ambiguous. Matches were found in the following scopes: SQL++ query context, FPL context. file:/Users/julestestard/Projects/svn/forward/2014-09-26-asterix-wrapper/src/ide/target/classes/edu/ucsd/forward/ide/function/security/invite_user.sql (56:29-56:36)
    edu.ucsd.forward.query.QueryCompilationException: Query path "username" is ambiguous. Matches were found in the following scopes: SQL++ query context, FPL context.
        at edu.ucsd.forward.query.ast.visitors.LogicalPlanBuilder.translateAttributeReference(LogicalPlanBuilder.java:2127)
        at edu.ucsd.forward.query.ast.visitors.LogicalPlanBuilder.translateValueExpression(LogicalPlanBuilder.java:1887)
        at edu.ucsd.forward.query.ast.visitors.LogicalPlanBuilder.translateGeneralFunctionNode(LogicalPlanBuilder.java:2618)

Troubleshooting done : 

 - I have verified all databases have been created and populated correctly according to descriptions found in documentation.
 - I have verfied Java version (1.6) and PostgreSQL version (9.1).

##8
It seems that by running the `TestNG - All` we have a successful run of the test suites for the query compiler. Yay!
