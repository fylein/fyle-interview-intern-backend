-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_assignment_count AS (
    SELECT teacher_id, COUNT(*) AS assignment_count
    FROM grades
    GROUP BY teacher_id
    ORDER BY assignment_count DESC
    LIMIT 1
)
SELECT COUNT(*) AS num_of_A_grades
FROM grades
WHERE grade = 'A'
AND teacher_id = (SELECT teacher_id FROM teacher_assignment_count);
