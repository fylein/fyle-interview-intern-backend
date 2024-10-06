-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH teacher_graded_counts AS (
    SELECT teacher_id, COUNT(*) AS graded_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_graded_teacher AS (
    SELECT teacher_id
    FROM teacher_graded_counts
    WHERE graded_count = (SELECT MAX(graded_count) FROM teacher_graded_counts)
    LIMIT 1
)
SELECT COUNT(*) AS grade_A_count
FROM assignments a
JOIN max_graded_teacher mgt ON a.teacher_id = mgt.teacher_id
WHERE a.grade = 'A' AND a.state = 'GRADED';