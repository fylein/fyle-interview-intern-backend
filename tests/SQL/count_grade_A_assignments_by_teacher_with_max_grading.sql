-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_assignment_counts AS (
    SELECT teacher_id, COUNT(*) AS num_graded
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_graded_teacher AS (
    SELECT teacher_id
    FROM teacher_assignment_counts
    ORDER BY num_graded DESC
    LIMIT 1
)
SELECT COUNT(*) AS num_grade_A
FROM assignments
WHERE grade = 'A'
AND teacher_id = (SELECT teacher_id FROM max_graded_teacher);


