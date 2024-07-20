# tests/principals_test.py
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
def h_principal():
    return {
        'X-Principal': json.dumps({
            'user_id': 5,
            'principal_id': 1
        })
    }

@pytest.fixture
def setup_data(client):
    """Fixture to set up test data."""
    # Add setup code here to insert test data into the database.
    response = client.post('/student/assignments', json={
        'content': 'Test assignment',
        'student_id': 1
    })
    assert response.status_code == 200
    assert 'data' in response.json
    assignment_id = response.json['data']['id']
    return assignment_id

def test_get_assignments(client, setup_data, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)
    assert response.status_code == 200

def test_grade_assignment(client, setup_data, h_principal):
    response = client.post('/principal/assignments/grade', headers=h_principal, json={
        'id': setup_data,
        'grade': 'A'
    })
    assert response.status_code == 200

def test_grade_assignment_invalid_grade(client, setup_data, h_principal):
    response = client.post('/principal/assignments/grade', headers=h_principal, json={
        'id': setup_data,
        'grade': 'InvalidGrade'
    })
    assert response.status_code == 400
