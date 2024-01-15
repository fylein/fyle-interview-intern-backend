-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH RankedTeachers AS (
    SELECT
        teacher_id,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_number
    FROM
        assignments
    WHERE
        teacher_id IS NOT NULL
        AND grade IS NOT NULL
    GROUP BY
        teacher_id
)
SELECT COUNT(*) AS grade_A_count
FROM assignments a
JOIN RankedTeachers rt ON a.teacher_id = rt.teacher_id
WHERE a.grade = 'A' AND rt.row_number = 1;