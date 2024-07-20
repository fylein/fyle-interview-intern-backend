import pytest
import json
from core.server import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///./test.sqlite3'
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def h_teacher_1():
    return {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 1
        })
    }

@pytest.fixture
def h_teacher_2():
    return {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 2
        })
    }

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get('/teacher/assignments', headers=h_teacher_1)
    assert response.status_code == 200

    data = response.json
    assert 'data' in data
    for assignment in data['data']:
        assert assignment['teacher_id'] == 1

def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get('/teacher/assignments', headers=h_teacher_2)
    assert response.status_code == 200

    data = response.json
    assert 'data' in data
    for assignment in data['data']:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

def test_grade_assignment_cross(client, h_teacher_2):
    """
    Failure case: Assignment 1 was submitted to teacher 1 and not teacher 2.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={"id": 1, "grade": "A"}
    )
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError' or data['error'] == 'ValidationError'  # Adjust as per actual error

def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    Failure case: API should allow only grades available in enum.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={"id": 1, "grade": "AB"}
    )
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    Failure case: If an assignment does not exist, check and throw 404.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={"id": 100000, "grade": "A"}
    )
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError' or data['error'] == 'NotFound'  # Adjust as per actual error

def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    Failure case: Only a submitted assignment can be graded.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={"id": 2, "grade": "A"}
    )
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError' or data['error'] == 'ValidationError'  # Adjust as per actual error
