-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH graded_assignments AS (
    SELECT teacher_id, COUNT(*) AS graded_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_graded_teacher AS (
    SELECT teacher_id
    FROM graded_assignments
    ORDER BY graded_count DESC
    LIMIT 1 
)
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM max_graded_teacher)
  AND grade = 'A';
