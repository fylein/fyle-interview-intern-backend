-- Write query to get number of graded assignments for each student:
SELECT 
    student_id,
    COUNT(assignment_id) AS graded_assignments_count
FROM 
    grades
GROUP BY 
    student_id;
