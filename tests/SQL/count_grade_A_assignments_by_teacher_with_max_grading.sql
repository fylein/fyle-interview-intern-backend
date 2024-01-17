WITH MaxGradedAssignments AS (
    SELECT
        teacher_id,
        COUNT(*) AS graded_count
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
    ORDER BY
        graded_count DESC
    LIMIT 1
)

SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    teacher_id = (SELECT teacher_id FROM MaxGradedAssignments)
    AND grade = 'A'
    AND state = 'GRADED';