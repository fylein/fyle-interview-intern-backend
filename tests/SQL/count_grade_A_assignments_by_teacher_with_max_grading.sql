-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_count AS (
    SELECT teacher_id, COUNT(*) AS total_graded_assignments
    FROM assignments
    WHERE state = 'GRADED'  
    GROUP BY teacher_id
),
max_grading_teacher AS (
    SELECT teacher_id
    FROM teacher_grading_count
    ORDER BY total_graded_assignments DESC
    LIMIT 1
)
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM max_grading_teacher)
AND grade = 'A';
