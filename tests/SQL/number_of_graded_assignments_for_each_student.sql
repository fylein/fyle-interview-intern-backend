-- Write query to get number of graded assignments for each student:
WITH TeacherAssignmentCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS assignment_count
    FROM
        assignments
    WHERE
        grade = 'A'
    GROUP BY
        teacher_id
),
TeacherMaxGrading AS (
    SELECT
        teacher_id
    FROM
        assignments
    WHERE
        grade IS NOT NULL
    GROUP BY
        teacher_id
    ORDER BY
        COUNT(*) DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS count_grade_A_assignments
FROM
    assignments AS a
JOIN
    TeacherMaxGrading AS tm ON a.teacher_id = tm.teacher_id
WHERE
    a.grade = 'A';
