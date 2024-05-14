-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- SELECT COUNT() AS num_grade_a
-- FROM assignments
-- WHERE grade='A' AND teacher_id in (SELECT teacher_id from assignments 
-- WHERE state='GRADED' and teacher_id IS NOT NULL
-- GROUP BY teacher_id
-- ORDER BY COUNT(*) DESC
-- LIMIT 1);


SELECT c1, c2, t1 FROM
(SELECT count(*) as c1, teacher_id as t1 FROM assignments
WHERE teacher_id and grade='A'
GROUP BY teacher_id ) as a INNER JOIN
(SELECT count(*) as c2, teacher_id as t2 FROM assignments
WHERE teacher_id --and state = 'GRADED' 
GROUP BY teacher_id ) as b 
ON a.t1=b.t2
ORDER BY c2 DESC, c1 DESC
;

-- SELECT 
--     COUNT(CASE WHEN a.grade = 'A' THEN 1 END) AS count_a,
--     COUNT(*) AS count_all,
--     a.teacher_id
-- FROM 
--     assignments a
-- WHERE 
--     a.teacher_id IS NOT NULL 
--     AND a.state = 'GRADED'
-- GROUP BY 
--     a.teacher_id
-- ORDER BY 
--     count_all DESC,
--     count_a DESC;
