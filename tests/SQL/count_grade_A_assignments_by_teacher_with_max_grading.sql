-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- Common Table Expression (CTE) to find the teacher ID with the most graded assignments
WITH MostGradedTeacher AS (
    -- Selects the teacher ID and counts the number of graded assignments for each teacher
    SELECT 
        teacher_id, 
        COUNT(*) AS num_graded_assignments 
    FROM 
        assignments 
    WHERE 
        state = 'GRADED' -- Considers only assignments that are graded
    GROUP BY 
        teacher_id 
    ORDER BY 
        num_graded_assignments DESC -- Orders the result by the count of graded assignments in descending order
    LIMIT 1 -- Limits the result to only one row, which represents the teacher with the most graded assignments
)
-- Selects the count of grade A's given by the teacher with the most graded assignments
SELECT 
    COUNT(*) AS grade_A_count
FROM 
    assignments 
WHERE 
    grade = 'A' -- Filters for assignments with grade A
    AND teacher_id = (SELECT teacher_id FROM MostGradedTeacher); -- Filters for assignments graded by the teacher with the most graded assignments

