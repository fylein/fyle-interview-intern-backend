import pytest
from controllers import GradeController
from models import Assignment

def test_grade_assignment():
    grade_controller = GradeController()
    assignment = Assignment.query.get(1)
    grade_controller.grade_assignment(assignment.id, 'A')
    assert assignment.grade == 'A'
