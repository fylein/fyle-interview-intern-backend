-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

select count(*) from assignments where grade is 'A' and teacher_id=:teacher_id and state is 'GRADED'


