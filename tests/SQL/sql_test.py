import random
from sqlalchemy import text, func
from sqlalchemy import or_ , and_

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

def get_grade_A_count_for_teacher_having_most_grade():
    stu_id_1_occ = Assignment.filter(and_(Assignment.state == AssignmentStateEnum.GRADED , Assignment.teacher_id == 1)).count()
    stu_id_2_occ = Assignment.filter(and_(Assignment.state == AssignmentStateEnum.GRADED , Assignment.teacher_id == 2)).count()
    
    # Return the count of grade A's given by the teacher with the most assignments
    if stu_id_1_occ < stu_id_2_occ:
        grade_a_count = Assignment.filter(and_(Assignment.grade == GradeEnum.A , Assignment.teacher_id == 2)).count()
    else:
        grade_a_count = Assignment.filter(and_(Assignment.grade == GradeEnum.A , Assignment.teacher_id == 1)).count()

    return grade_a_count



def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
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

    # Commit changes to the database
    db.session.commit()

    return 1


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments = Assignment.filter(or_(Assignment.student_id == 1, Assignment.student_id == 2)).all()

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        if assignment.state == AssignmentStateEnum.SUBMITTED:
            assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state  
            assignment.grade = random.choice(list(GradeEnum))

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    stu_id_1_occ = Assignment.filter(and_(Assignment.state == AssignmentStateEnum.GRADED , Assignment.student_id == 1)).count()
    stu_id_2_occ = Assignment.filter(and_(Assignment.state == AssignmentStateEnum.GRADED , Assignment.student_id == 2)).count()
    # Define the expected result before any changes
    expected_result = [(1, stu_id_1_occ),(2, stu_id_2_occ)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]
        assert result[1] == sql_result[itr][1]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    create_n_graded_assignments_for_teacher(5)

    grade_a_count_1 = get_grade_A_count_for_teacher_having_most_grade()
    
    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    if sql_result:
        assert grade_a_count_1 == sql_result[0][0]
    else:   
        assert grade_a_count_1 == 0

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    create_n_graded_assignments_for_teacher(10, 2)

    grade_a_count_2 = get_grade_A_count_for_teacher_having_most_grade()

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    if sql_result:
        assert grade_a_count_2 == sql_result[0][0]
    else:   
        assert grade_a_count_2 == 0