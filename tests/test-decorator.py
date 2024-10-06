import json
from flask import Flask, jsonify, request
import pytest

from core.apis.decorators import authenticate_principal, accept_payload
from core.libs import assertions  # This would raise the required assertions in case of errors

app = Flask(__name__)


@app.route('/student/assignments', methods=['GET'])
@authenticate_principal
def student_assignments(principal):
    return jsonify({"message": "Student assignments"}), 200

@app.route('/teacher/dashboard', methods=['GET'])
@authenticate_principal
def teacher_dashboard(principal):
    return jsonify({"message": "Teacher dashboard"}), 200

@app.route('/principal/dashboard', methods=['GET'])
@authenticate_principal
def principal_dashboard(principal):
    return jsonify({"message": "Principal dashboard"}), 200


# Now we write test cases
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_authenticate_principal_no_header(client):
    """Test the decorator when no 'X-Principal' header is provided."""
    response = client.get('/student/assignments')
    assert response.status_code == 401
    assert response.json['error'] == 'principal not found'


def test_authenticate_principal_malformed_header(client):
    """Test the decorator when the 'X-Principal' header is malformed."""
    headers = {
        'X-Principal': 'Invalid JSON'  
    }
    response = client.get('/student/assignments', headers=headers)
    assert response.status_code == 400  


def test_authenticate_principal_invalid_path(client):
    """Test the decorator for an invalid API path."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': None,
            'teacher_id': None,
            'principal_id': None
        })
    }
    response = client.get('/invalid-path', headers=headers)
    assert response.status_code == 404  
    assert response.json['error'] == 'No such api'


def test_authenticate_principal_missing_principal_id(client):
    """Test when requesting a /principal endpoint without a principal_id."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': None,
            'teacher_id': None,
            'principal_id': None  
        })
    }
    response = client.get('/principal/dashboard', headers=headers)
    assert response.status_code == 401  
    assert response.json['error'] == 'requester should be a principal'


def test_authenticate_principal_missing_student_id(client):
    """Test when requesting a /student endpoint without a student_id."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': None,  
            'teacher_id': None,
            'principal_id': None
        })
    }
    response = client.get('/student/dashboard', headers=headers)
    assert response.status_code == 401  
    assert response.json['error'] == 'requester should be a student'


def test_authenticate_principal_valid_teacher(client):
    """Test when requesting a /teacher endpoint with valid teacher_id."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': None,
            'teacher_id': 10,  
            'principal_id': None
        })
    }
    response = client.get('/teacher/dashboard', headers=headers)
    assert response.status_code == 200  
    assert response.json['message'] == 'Teacher dashboard'


def test_authenticate_principal_valid_student(client):
    """Test when requesting a /student endpoint with valid student_id."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': 10,  
            'teacher_id': None,
            'principal_id': None
        })
    }
    response = client.get('/student/assignments', headers=headers)
    assert response.status_code == 200  
    assert response.json['message'] == 'Student assignments'


def test_authenticate_principal_valid_principal(client):
    """Test when requesting a /principal endpoint with valid principal_id."""
    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'student_id': None,
            'teacher_id': None,
            'principal_id': 10  
        })
    }
    response = client.get('/principal/dashboard', headers=headers)
    assert response.status_code == 200  
    assert response.json['message'] == 'Principal dashboard'





