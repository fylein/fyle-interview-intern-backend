-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS num_grade_a
FROM assignments a
JOIN teachers t ON a.teacher_id = t.id
WHERE a.grade = 'A'
AND t.id = (
    SELECT teacher_id
    FROM assignments
    GROUP BY teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);