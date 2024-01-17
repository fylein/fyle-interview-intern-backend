-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH GradingCounts AS (
    SELECT
        teacher_id,
        grade,
        COUNT(*) AS grade_count
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id, grade
)
SELECT
    MAX(grade_count) AS max_grade_count
FROM
    GradingCounts
WHERE
    grade = 'A'