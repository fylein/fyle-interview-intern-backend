-- Write query to find the nCopy code
WITH GradingCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS grading_count
    FROM
        assignments
    WHERE
        grade = 'A'
    GROUP BY
        teacher_id
)

SELECT
    a.teacher_id,
    COUNT(*) AS grade_A_assignments_count
FROM
    assignments a
JOIN
    GradingCounts gc ON a.teacher_id = gc.teacher_id
WHERE
    a.grade = 'A'
    AND gc.grading_count = (
        SELECT
            MAX(grading_count)
        FROM
            GradingCounts
    )
GROUP BY
    a.teacher_id;umber of grade A's given by the teacher who has graded the most assignments
