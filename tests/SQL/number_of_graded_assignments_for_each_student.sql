-- tests/SQL/number_of_graded_assignments_for_each_student.sql
SELECT
    student_id,
    COUNT(*)
FROM
    assignments
WHERE
    state = 'GRADED'
GROUP BY
    student_id;
