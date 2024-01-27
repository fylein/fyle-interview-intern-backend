-- Write query to get number of assignments for each state
select state, count(*) from assignments group by state;