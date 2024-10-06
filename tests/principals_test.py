import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
from core import create_app
from flask import json


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED, AssignmentStateEnum.DRAFT]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'Cannot grade an assignment in DRAFT state' in response.json['error']


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C.value


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 8,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B



def test_grade_assignment_nonexistent(client, h_principal):
    """
    Test that grading a non-existent assignment returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 9999, 'grade': GradeEnum.A.value},
        headers=h_principal
    )

    assert response.status_code == 404
    assert response.json['error'] == 'Assignment not found'


def test_grade_assignment_missing_parameters(client, h_principal):
    """
    Test that missing parameters in the grading request returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'grade': GradeEnum.A.value},  # Missing 'id'
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Missing 'id' in the request"

def test_grade_assignment_non_json_payload(client, h_principal):
    """
    Test that sending a non-JSON payload returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        data='This is not JSON',
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == 'Invalid content type'

def test_grade_assignment_empty_payload(client, h_principal):
    """
    Test that an empty payload returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={},
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Missing 'id' or 'grade' in the request"


def test_grade_assignment_invalid_assignment_id(client, h_principal):
    """
    Test that providing an invalid assignment ID returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': -1, 'grade': GradeEnum.B.value},  
        headers=h_principal
    )

    assert response.status_code == 404
    assert response.json['error'] == 'Assignment not found'

def test_missing_x_principal_header(client):
    response = client.get('/principal/teachers')
    assert response.status_code == 400
    assert response.json == {"error": "Missing X-Principal header"}

def test_invalid_x_principal_header_json(client):
    headers = {
        'X-Principal': 'invalid-json'
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid X-Principal header"}


def test_missing_principal_id_in_x_principal_header(client):
    headers = {
        'X-Principal': json.dumps({})
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid X-Principal header"}


def test_invalid_principal_id_in_x_principal_header(client):
    headers = {
        'X-Principal': json.dumps({"principal_id": "invalid-id"})
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid principal_id"}


def test_empty_principal_id_in_x_principal_header(client):
    headers = {
        'X-Principal': json.dumps({"principal_id": ""})
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid principal_id'}


def test_multiple_teachers_for_principal(client):
    headers = {
        'X-Principal': json.dumps({"principal_id": 1})  
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json['data'], list)
    assert len(response.json['data']) > 1  


def test_invalid_data_type_for_principal_id(client):
    headers = {
        'X-Principal': json.dumps({"principal_id": "not-an-integer"})  
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid principal_id'}


def test_get_assignments_no_data(client, h_principal_1):
    """
    Test when no assignments are found for the principal.
    """
    response = client.get(
        '/principal/assignments',
        headers=h_principal_1
    )

    assert response.status_code == 404
    assert response.json['message'] == "No assignments found for this principal."


def test_invalid_x_principal_header_post(client):
    """
    Test invalid X-Principal header during POST request.
    """
    headers = {'X-Principal': 'invalid-json'}
    response = client.post('/principal/assignments/grade', json={'id': 1, 'grade': GradeEnum.A.value}, headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid X-Principal header"}


def test_grade_assignment_unauthorized_principal(client, h_principal_1):
    """
    Test unauthorized principal trying to grade an assignment.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 2, 'grade': GradeEnum.A.value},
        headers=h_principal_1
    )

    assert response.status_code == 403
    assert response.json['error'] == "Unauthorized: Assignment does not belong to the principal"

def test_grade_assignment_invalid_grade(client, h_principal):
    """
    Test grading with an invalid grade value.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 3, 'grade': 'InvalidGrade'},  
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Invalid grade provided"

def test_empty_x_principal_header(client):
    """
    Test missing X-Principal header.
    """
    response = client.get('/principal/assignments')
    assert response.status_code == 400
    assert response.json['error'] == "Missing X-Principal header"


def test_invalid_json_structure_x_principal(client):
    """
    Test invalid JSON structure in X-Principal header.
    """
    headers = {'X-Principal': 'invalid-json-structure'}
    response = client.get('/principal/assignments', headers=headers)
    assert response.status_code == 400
    assert response.json['error'] == "Invalid X-Principal header"


def test_missing_grade_in_request(client, h_principal):
    """
    Test missing grade in the request body when grading an assignment.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 1},  # No grade field
        headers=h_principal
    )
    assert response.status_code == 400
    assert response.json['error'] == "Missing 'grade' in the request"


def test_invalid_assignment_id(client, h_principal):
    """
    Test non-existent assignment ID.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 9999, 'grade': GradeEnum.A.value},  
        headers=h_principal
    )
    assert response.status_code == 404
    assert response.json['error'] == "Assignment not found"

def test_grade_already_graded_assignment(client, h_principal):
    """
    Test that an already graded assignment cannot be graded again.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,  
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
   
def test_grade_assignment_invalid_grade_value(client, h_principal):
    """
    Test that grading with an invalid grade value returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 1, 'grade': 'InvalidGradeValue'},  
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Invalid grade provided"

def test_grade_assignment_below_minimum(client, h_principal):
    """
    Test that assigning a grade below the minimum allowed returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 1, 'grade': 'D-'},  
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Invalid grade provided"


def test_grade_assignment_missing_id(client, h_principal):
    """
    Test that missing ID in the grading request returns an error.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'grade': GradeEnum.B.value},  
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Missing 'id' in the request"

def test_principal_no_assignments(client, h_principal_1):
    """
    Test that the principal returns a 404 when no assignments are available.
    """
    response = client.get(
        '/principal/assignments',
        headers=h_principal_1
    )

    assert response.status_code == 404
    assert response.json['message'] == "No assignments found for this principal."
