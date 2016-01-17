// Find all students enrolled in the course with id = 101

List listStudents = [];
int i = 0;
List students = Query("SELECT * FROM Students");
List enrolled101 = Query(
    "SELECT sid FROM enrollments WHERE cid = 101");
while ( i < students.size() ) {
    if (enrolled101.contains(students[i].sid)) {
        listStudents = append(listStudents, students[i]);
    }
    ++i;}
