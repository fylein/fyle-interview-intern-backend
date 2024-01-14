-- Write query to get number of assignments for each state
select count(state) as number_of_assignments from
assignments group by state;

