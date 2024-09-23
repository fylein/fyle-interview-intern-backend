import random
from sqlalchemy import text
from core import db, app  # Import the app object
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
import pytest

@pytest.fixture(autouse=True)
def setup_function():
    with app.app_context():
        db.session.query(Assignment).delete()
        db.session.commit()

def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    for _ in range(number):
        grade = random.choice(list(GradeEnum))
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )
        db.session.add(assignment)
        if grade == GradeEnum.A:
            grade_a_counter += 1

    db.session.commit()
    return grade_a_counter

def test_get_assignments_in_graded_state_for_each_student():
    with app.app_context():  # Wrapping test in app context
        create_n_graded_assignments_for_teacher(3, teacher_id=1)  
        submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)
        for assignment in submitted_assignments:
            assignment.state = AssignmentStateEnum.GRADED

        db.session.flush()
        db.session.commit()

        expected_result = [(1, 3)]
        with open('SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
            sql = fo.read()

        sql_result = db.session.execute(text(sql)).fetchall()
        for itr, result in enumerate(expected_result):
            assert result[0] == sql_result[itr][0]

def test_get_grade_A_assignments_for_teacher_with_max_grading():
    with app.app_context():  # Wrapping test in app context
        
        # Create graded assignments for teacher 1
        grade_a_count_1 = create_n_graded_assignments_for_teacher(5, 1)
        
        # Create graded assignments for teacher 2
        create_n_graded_assignments_for_teacher(5, 2)

        # Determine the teacher_id with the maximum number of graded assignments
        max_teacher_id_query = """
        SELECT teacher_id
        FROM assignments
        GROUP BY teacher_id
        ORDER BY COUNT(*) DESC
        LIMIT 1;
        """
        
        max_teacher_id_result = db.session.execute(text(max_teacher_id_query)).fetchone()
        max_teacher_id = max_teacher_id_result[0] if max_teacher_id_result else None

        # Now execute the SQL for counting grade A assignments
        with open('SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
            sql = fo.read()

        # Pass the teacher_id as a parameter
        sql_result = db.session.execute(text(sql), {'teacher_id': max_teacher_id}).fetchall()

        # Assert the expected count of grade A assignments
        assert grade_a_count_1 == sql_result[0][0]

        # Optionally, you can repeat this for teacher 2
        # and assert on the expected count for their grade A assignments

