import pytest
import json
from core.server import create_app  # Import the create_app function

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
def h_student_1():
    return {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

@pytest.fixture
def h_student_2():
    return {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

def test_get_assignments_student_1(client, h_student_1):
    response = client.get('/student/assignments', headers=h_student_1)
    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1

def test_get_assignments_student_2(client, h_student_2):
    response = client.get('/student/assignments', headers=h_student_2)
    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

def test_post_assignment_null_content(client, h_student_1):
    """
    Failure case: Content cannot be null.
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': None}
    )
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'
    assert response.json['message'] == 'Content cannot be null'

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': content}
    )
    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': 2, 'teacher_id': 2}
    )
    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_assignment_resubmit_error(client, h_student_1):
    """
    Failure case: Submitting an assignment that is not in a draft state should fail.
    """
    # First, submit the assignment to change its state to SUBMITTED
    client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': 2, 'teacher_id': 2}
    )

    # Try submitting the same assignment again
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': 2, 'teacher_id': 2}
    )
    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Only a draft assignment can be submitted'
