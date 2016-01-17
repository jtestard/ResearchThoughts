// Find all students and the list of cids
// of all the courses in which they are enrolled,
// including students with no courses.

List listSC := []
int i := 0;
List students := Query("SELECT * FROM Students");
List enrollments := Query("SELECT sid, cid FROM Enrollments");
while (i < students.size()) {
   List cids := [];
    while (j < enrollments.size() ) {
        if (students[i].sid := enrollments[j].sid) {
            cids := append(cids, enrollments[j].cid);
        }
        j++;
    }
   listSC := append(listSC, append(
     students[i], append(cids, [])));
   i++;
}
