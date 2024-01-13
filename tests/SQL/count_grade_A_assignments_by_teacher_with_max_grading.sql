-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS GradeACount
FROM Grades
WHERE Grade = 'A'
AND TeacherID = (
    SELECT TOP 1 TeacherID
    FROM Grades
    GROUP BY TeacherID
    ORDER BY COUNT(*) DESC
);
