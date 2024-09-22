-- Write query to get number of graded assignments for each student:
select student_id,count(*) as graded_assignments_count 
from assignments
WHERE state = 'GRADED'
GROUP BY student_id;
