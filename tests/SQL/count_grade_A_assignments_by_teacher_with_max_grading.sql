-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH graded_assignments AS (
    SELECT teacher_id, COUNT(*) AS count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
teacher_grades AS (
    SELECT a.teacher_id, COUNT(*) AS grade_count
    FROM assignments a
    INNER JOIN (SELECT teacher_id FROM graded_assignments WHERE count = (SELECT MAX(count) FROM graded_assignments)) t
    ON a.teacher_id = t.teacher_id
    WHERE a.grade = 'A'
    GROUP BY a.teacher_id
)
SELECT COALESCE(SUM(grade_count), 0) AS grade_count
FROM teacher_grades;
