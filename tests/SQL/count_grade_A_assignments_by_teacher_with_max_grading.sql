-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

WITH TeacherAssignmentCount AS (
    -- Step 1: Find the teacher who graded the most assignments
    SELECT teacher_id, COUNT(*) AS graded_assignments
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    ORDER BY graded_assignments DESC
    LIMIT 1
)
-- Step 2: Count the number of grade A's given by that teacher
SELECT COUNT(*) AS grade_A_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM TeacherAssignmentCount)
  AND grade = 'A'
  AND state = 'GRADED';
