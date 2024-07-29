-- Write query to get number of graded assignments for each student:
select student_id, count(*)
from assignments
where state='GRADED'
group by student_id