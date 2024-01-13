-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT MAX(count_grade) AS max_grade
FROM (
    SELECT teacher_id, COUNT(grade) AS count_grade
    FROM assignments
    WHERE grade = 'A' AND state = 'GRADED'
    GROUP BY teacher_id
) AS grade_counts;