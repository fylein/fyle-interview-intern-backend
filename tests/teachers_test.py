from core import db
from sqlalchemy import text
import datetime
from core.models.teachers import Teacher

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_grade_assignment_cross(client, h_teacher_1):
    """
    failure case: assignment 3 was submitted to teacher 2 and not teacher 1
    """

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 3,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
    assert data['message'] == 'This assignment belongs to some other teacher'


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

    assert data['error'] == 'FyleError'


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

def test_grade_assignment_invalid_teacher(client, h_teacher_2):

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400


def test_grade_assignment_success(client, h_teacher_2, h_student_2):

    # Submit an assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            "id": 3,
            "teacher_id": 2
        }
    )

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 3,
            "grade": "B"
        }
    )


    db.engine.execute(text("UPDATE assignments SET grade = NULL, state = 'DRAFT' WHERE id = 3"))
    db.session.commit()

    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == 'B'

    # Set grade to NULL and state to SUBMITTED
    db.engine.execute(text("UPDATE assignments SET grade = NULL, state = 'SUBMITTED' WHERE id = 900"))
    #db.session.commit()

def test_teacher_model(client):
    teachers = Teacher.get_all()
    assert len(teachers) == 2

    teacher = teachers[0]
    assert teacher.id == 1
    assert teacher.user_id == 3
    assert isinstance(teacher.created_at, datetime.datetime)
    assert isinstance(teacher.updated_at, datetime.datetime)

def test_grade_assignment_invalid_request_body(client, h_teacher_2):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "student_id": 1
        }
    )

    assert response.status_code == 400
    assert "Missing data for required field." in response.json["message"] 

def test_teacher_model_repr(client):
    teacher = Teacher.query.get(1)
    assert teacher.__repr__() == '<Teacher 1>'