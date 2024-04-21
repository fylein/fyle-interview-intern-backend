-- -- Write query to find the number of grade A's given by the teacher who has graded the most assignments

/*
 constraints: 
 > we cant use vars in sqlite.
 > we cant nest queries. {sqlalchemy exception} tried creating a temp table and put the id of the mvp teacher in it but it didnt work.
*/

SELECT
    COUNT(*) AS no_of_As
FROM
    assignments
WHERE
    grade == 'A'
GROUP BY
    teacher_id
ORDER BY
    no_of_As DESC;