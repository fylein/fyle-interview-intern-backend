from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from core import db, create_app

def test_repr():
    assignment = Assignment(id=1)
    assert repr(assignment) == '<Assignment 1>'


