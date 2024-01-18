-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = (
    SELECT teacher_id
    FROM (
        SELECT teacher_id, COUNT(*) AS assignment_count
        FROM assignments
        WHERE grade is not NULL AND state='GRADED'
        GROUP BY teacher_id
        ORDER BY assignment_count DESC
        LIMIT 1
    ) AS subquery
)
AND grade = 'A';


