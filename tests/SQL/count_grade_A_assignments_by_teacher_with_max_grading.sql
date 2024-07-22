-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradedCounts AS (
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
    COUNT(*) AS grade_A_count
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM TeacherGradedCounts)
    AND grade = 'A';
