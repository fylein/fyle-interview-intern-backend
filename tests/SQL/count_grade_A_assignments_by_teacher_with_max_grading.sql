-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_assignment_counts AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments
    FROM 
        assignments
    GROUP BY 
        teacher_id
),
teacher_with_max_assignments AS (
    SELECT 
        teacher_id
    FROM 
        teacher_assignment_counts
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
SELECT 
    COUNT(*) AS grade_A_count
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM teacher_with_max_assignments)
    AND grade = 'A';
