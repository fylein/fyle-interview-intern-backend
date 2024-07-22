-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherAssignments AS (
    SELECT
        teacher_id,
        COUNT(id) AS total_assignments
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
),
TopTeacher AS (
    SELECT
        teacher_id
    FROM
        TeacherAssignments
    ORDER BY
        total_assignments DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    grade = 'A'
    AND teacher_id = (SELECT teacher_id FROM TopTeacher);
