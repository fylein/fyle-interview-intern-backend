-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS grade_a
FROM assignments AS a
WHERE a.grade = 'A'
AND a.teacher_id = (
    SELECT a.teacher_id
    FROM assignments AS a
    WHERE a.state = 'GRADED'
    GROUP BY a.teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

