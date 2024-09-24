import random
from sqlalchemy import text
import sqlalchemy
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


import random
from sqlalchemy.orm import sessionmaker

def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter

def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all assignments for student 1 and change their state to 'GRADED'
    submitted_assignments = Assignment.query.filter(Assignment.student_id == 1).all()

    assert submitted_assignments, "No assignments found for student 1"

    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED

    db.session.commit()

    expected_result = [(1, len(submitted_assignments))]

    # Execute the SQL query and compare the result with the expected result
    try:
        with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
            sql = fo.read()

        # Ensure the SQL query is a SELECT statement and returns results
        sql_result = db.session.execute(text(sql)).fetchall()
        assert sql_result, "SQL query returned no results"

        for itr, result in enumerate(expected_result):
            assert result == sql_result[itr], f"Expected {result}, got {sql_result[itr]}"

    except sqlalchemy.exc.ResourceClosedError:
        raise AssertionError("SQL query did not return any data. Ensure it is a SELECT query.")
    except Exception as e:
        raise AssertionError(f"SQL query failed with error: {e}")



def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
    
    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_1 == sql_result[0][0]

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_2 == sql_result[0][0]