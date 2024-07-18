-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
),
MaxGradingTeacher AS (
    SELECT
        teacher_id
    FROM
        TeacherGradingCounts
    ORDER BY
        total_graded DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    teacher_id = (SELECT teacher_id FROM MaxGradingTeacher)
    AND grade = 'A';
