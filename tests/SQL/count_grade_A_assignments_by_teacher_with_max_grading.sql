-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
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
