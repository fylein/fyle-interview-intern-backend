-- Write query to get number of graded assignments for each student:
-- -- Write query to get number of graded assignments for each student:
-- from core.models.assignments import Assignment
-- from core.models.assignments import AssignmentStateEnum
-- sql_query = """
--     SELECT student_id, COUNT(*) AS num_graded_assignments
--     FROM Assignment
--     WHERE state = 'GRADED'
--     GROUP BY student_id;
-- """
-- Get the number of graded assignments for each student
SELECT 
    student_id, 
    COUNT(*) AS num_graded_assignments
FROM 
    assignments
WHERE 
    state = 'GRADED'
GROUP BY 
    student_id;