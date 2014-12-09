## Asterix SQL++ Interface Workflow

### The asterix-sqlpp project
The `asterix-sqlpp` project contains the code for the SQL++ parser.

### The 

	@edu.uci.ics.asterix.api.http.servlet.RESTAPIServlet
		handleRequest(HTTPRequest, String query)
		// Hyracks and Session config not shown
		List<Statement> stmts = (new AQLParser(query)).parse();
		(new aqlTranslator(stmts)).compileAndExecute();
	@edu.uci.ics.asterix.aql.translator.AqlTranslator
		handleQuery(query);
		ewriteCompileQuery(query);
		rewrittenQuery = APIFramework.reWriteQuery(query)
		Hyracks.JobSpecification compiled = APIFramework.compileQuery(rewrittenQuery);


Plan of presentation :

1) Show current state of progress :

 - Parser done for non-nested SFW queries with no complex values (handles INNER and OUTER Joins).
 - Tests available and bundle shippable.

2) Show what needs to be done next :

 - Show AST and logical plan comparison.
 - Say that currently the translation details are still fuzzy.