from core.models.assignments import Assignment,AssignmentStateEnum ,GradeEnum
from core.apis.decorators import AuthPrincipal
import pytest

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

def test_get_assignments_by_teacher():
    teacher_id = 1
    assignments = Assignment.get_assignments_by_teacher(teacher_id)
    assert all(assignment.teacher_id == teacher_id for assignment in assignments)


def test_grade_assignment_invalid_id(client, h_teacher_1):
    """
    failure case: grading an assignment with invalid ID should return 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": -1,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

def test_list_assignments_forbidden(client, h_student):
    """
    failure case: a student trying to access teacher's assignments should return 403
    """
    response = client.get('/teacher/assignments', headers=h_student)

    assert response.status_code == 403
    data = response.json

def test_list_assignments_unauthorized(client):
    """
    failure case: accessing assignments without authorization should return 401
    """
    response = client.get('/teacher/assignments')

    assert response.status_code == 401
    data = response.json


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 12,
            "grade": "B"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'



@pytest.fixture
def auth_teacher_2():
    return AuthPrincipal(user_id=2, teacher_id=2)

def test_mark_grade_success(auth_teacher_2):
    """
    success case: grade an assignment successfully
    """
    graded_assignment = Assignment.mark_grade(
        _id=1,
        grade=GradeEnum.A,
        auth_principal=auth_teacher_2
    )

    assert graded_assignment.grade == GradeEnum.A
    assert graded_assignment.state == AssignmentStateEnum.GRADED