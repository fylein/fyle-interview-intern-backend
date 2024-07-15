 -- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS num_a_grades
FROM assignments a
JOIN (
    SELECT teacher_id
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
) most_active_teacher ON a.teacher_id = most_active_teacher.teacher_id
WHERE a.grade = 'A';