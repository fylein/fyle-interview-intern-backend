-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH teacher_grades AS (
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
max_grading_teacher AS (
    SELECT
        teacher_id
    FROM
        teacher_grades
    WHERE
        total_graded = (SELECT MAX(total_graded) FROM teacher_grades)
)
SELECT
    COUNT(*)
FROM
    assignments
WHERE
    teacher_id IN (SELECT teacher_id FROM max_grading_teacher)
    AND grade = 'A';
