from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

def test_grade_assignment_bad_assignment(client, h_principal):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 100000,
            "grade": "A"
        }
    )
    
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'

def test_grade_assignment_bad_grade(client, h_principal):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200

    data = response.json['data']
    
import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum

@pytest.mark.parametrize("invalid_payload", [
    {},
    {'grade': GradeEnum.A.value},
    {'id': 1},
    {'id': 'not_an_int', 'grade': GradeEnum.A.value},
    {'id': 1, 'grade': 'not_a_valid_grade'},
])
def test_grade_assignment_invalid_payload(client, h_principal, invalid_payload):
    """Test grading an assignment with invalid payload"""
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json=invalid_payload
    )

    assert response.status_code == 400
    assert 'error' in response.json


def test_unauthorized_access(client):
    """Test accessing principal endpoints without authentication"""
    endpoints = [
        ('/principal/assignments', 'GET'),
        ('/principal/assignments/grade', 'POST'),
        ('/principal/teachers', 'GET')
    ]

    for endpoint, method in endpoints:
        if method == 'GET':
            response = client.get(endpoint)
        elif method == 'POST':
            response = client.post(endpoint, json={})
        
        assert response.status_code == 401

def test_grade_assignment_all_grades(client, h_principal):
    """Test grading assignments with all possible grades"""
    for grade in GradeEnum:
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 1,
                'grade': grade.value
            },
            headers=h_principal
        )

        assert response.status_code == 200
        assert response.json['data']['grade'] == grade.value
