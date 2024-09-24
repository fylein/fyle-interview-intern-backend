-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCount AS (
    SELECT 
        teacher_id, 
        COUNT(*) AS total_assignments
    FROM 
        assignments
    GROUP BY 
        teacher_id
),
MaxGradingTeacher AS (
    SELECT 
        teacher_id
    FROM 
        TeacherGradingCount
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
SELECT 
    COUNT(*) AS grade_A_count
FROM 
    assignments
WHERE 
    grade = 'A'
    AND teacher_id = (SELECT teacher_id FROM MaxGradingTeacher);