-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- Step 1: Find the teacher who has graded the most assignments
WITH TeacherAssignmentCount AS (
    SELECT 
        a.teacher_id,
        COUNT(*) AS assignment_count
    FROM assignments a
    GROUP BY a.teacher_id
),
TopTeacher AS (
    SELECT 
        teacher_id
    FROM TeacherAssignmentCount
    ORDER BY assignment_count DESC
    LIMIT 1
)

-- Step 2: Count the number of grade A's given by this teacher
SELECT 
    COUNT(*) AS grade_A_count
FROM grades g
JOIN assignments a ON g.assignment_id = a.assignment_id
JOIN TopTeacher tt ON a.teacher_id = tt.teacher_id
WHERE g.grade = 'A';
