-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COALESCE(SUM(CASE WHEN a.grade = 'A' THEN 1 ELSE 0 END), 0) AS grade_a_count
FROM assignments a
JOIN (
    SELECT teacher_id
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    HAVING COUNT(*) = (
        SELECT MAX(graded_count)
        FROM (
            SELECT COUNT(*) AS graded_count
            FROM assignments
            WHERE state = 'GRADED'
            GROUP BY teacher_id
        ) AS counts
    )
) AS top_teachers ON a.teacher_id = top_teachers.teacher_id
WHERE a.state = 'GRADED';