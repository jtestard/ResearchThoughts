## Asterix SQL++ TODO list

### Urgent

 - Fix bug already started on Asterix website (concerns complex equality).
 - Build the parser for SQL++ with :
   - All expressions required to cover the entirety of SQL++ queries.
   - All non-query statements from AQL.
 - Do refactoring of API Framework as described in emails.
 - Understand how variable resolution works for AQL and SQL++ RI and have something smart for Asterix SQL++.
 - Handle transactions in SQL++ interface.

### Soon

 - Add a "print optimized logical plan" (with an actual logical plan, not a physical plan). See issue posted on Asterix website.

### Low priority

 - Add SQL++ rewriting for cases shown in emails.