-- Write query to get number of assignments for each state
SELECT state,count(*) from assignments group by state