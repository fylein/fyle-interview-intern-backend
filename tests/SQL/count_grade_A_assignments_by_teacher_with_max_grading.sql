-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
select count(*) from assignments
where grade=='A'
and teacher_id==(
    select teacher_id
    from assignments
    group by teacher_id
    order by count(*) desc
    limit 1
)