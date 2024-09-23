--Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(id) as num_grade_A
FROM assignments
WHERE grade = 'A' AND teacher_id = (
    SELECT teacher_id
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    ORDER BY COUNT(id) DESC
    LIMIT 1
);