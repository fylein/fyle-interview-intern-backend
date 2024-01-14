-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
select max(count_grade) as max_grade
from (
    select teacher_id, COUNT(grade) as count_grade
    from assignments
    where grade='A' AND state='GRADED'
    group by teacher_id
) as grade_counts;
