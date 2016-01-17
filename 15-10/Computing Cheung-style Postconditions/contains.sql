SELECT s
FROM students s
WHERE s.sid = (
    SELECT sid
    FROM enrollments
    WHERE cid = 101
)
ORDER BY s.sid
