-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher as (
    SELECT teacher_id, COUNT(*) AS a_grade_count
    FROM assignments
    WHERE grade IS NOT NULL AND teacher_id IS NOT NULL
    GROUP BY teacher_id
    ORDER BY a_grade_count DESC
    LIMIT 1
    )
SELECT count(*) as a_grade_count
FROM teacher JOIN assignments using(teacher_id)
WHERE grade = 'A';