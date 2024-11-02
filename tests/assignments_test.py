from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs.exceptions import FyleError
import pytest
from core.apis.decorators import AuthPrincipal


def test_upsert_assignment_fyle_error():
    with pytest.raises(FyleError):
        Assignment.upsert(
            Assignment(id=99, content="test", state=AssignmentStateEnum.SUBMITTED)
        )


def test_upsert_assignment_bad_input():
    try:
        Assignment.upsert("test")
    except FyleError as e:
        assert e.message == "'str' object has no attribute 'id'"


def test_mark_grade_fyle_error():
    with pytest.raises(FyleError):
        Assignment.mark_grade(99, 100, None)


def test_mark_grade_bad_input():
    try:
        Assignment.mark_grade(1, 1, None)
    except FyleError as e:
        assert e.message == "'NoneType' object has no attribute 'teacher_id'"


def test_re_grade_belongs_to_other_teacher():
    principal = AuthPrincipal(teacher_id=1, user_id=1)
    try:
        Assignment.re_grade(1, "A", principal)
    except FyleError as e:
        assert e.message == "This assignment belongs to some other teacher"


def test_repr():
    assignment = Assignment()
    assert assignment.__repr__() == "<Assignment None>"
