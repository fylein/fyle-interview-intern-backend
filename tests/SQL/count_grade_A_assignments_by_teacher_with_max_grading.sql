-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
with teacher_grade_count as(
    select teacher_id , count(*) as no_of_assignments_graded
    from assignments
    where state='GRADED'
    group by teacher_id
),

teacher_with_maximum_grading as (
    select teacher_id
    from teacher_grade_count
    order by no_of_assignments_graded desc
    limit 1
)

select count(*) as grade_A_assignments_by_teacher_with_max_grading
from assignments
where teacher_id in (select teacher_id from teacher_with_maximum_grading) and state='GRADED' and grade='A'