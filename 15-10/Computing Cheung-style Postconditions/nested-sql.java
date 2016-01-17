listSC = forward.executeQuery(
"SELECT s, (" +
"    SELECT c.cid" +
"    FROM Courses AS c" +
"    WHERE c.sid = s.sid" +
"    ORDER BY c.sid" +
") AS cids" +
"FROM Students AS s" +
"ORDER BY s.sid;"
);
