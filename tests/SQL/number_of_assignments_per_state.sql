-- Write query to get number of assignments for each state
Select state , COUNT(*) as StateCount from assignments group by state