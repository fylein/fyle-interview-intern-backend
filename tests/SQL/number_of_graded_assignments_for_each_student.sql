-- Write query to get number of graded assignments for each student:
select count(*) from assignments where STATE='GRADED' group by student_id