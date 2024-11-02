from core.models.assignments import AssignmentStateEnum, GradeEnum
from core import db
from core.models.assignments import Assignment
import json
from core.models.principals import Principal

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
    # Make the assignment draft
    Assignment.query.filter_by(id=5).update({'state': AssignmentStateEnum.DRAFT})
    db.session.commit()
    
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    assert response.status_code == 400


def test_grade_assignment(client, h_principal, h_student_2, h_teacher_2):
    
    # Set the assignment to submitted state
    response = client.post(
        '/student/assignments/submit',
        json={
            'id': 4,
            'teacher_id': 2
        },
        headers=h_student_2
    )

    # Grade the assignment
    response = client.post(
        "/teacher/assignments/grade",
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        },
        headers=h_teacher_2
    )

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    # Set the assignment to draft state
    Assignment.query.filter_by(id=4).update({'state': AssignmentStateEnum.DRAFT})
    db.session.commit()

    assert response.status_code == 200


def test_list_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

def test_grade_assignment_submitted(client, h_principal):
    """
    failure case: If an assignment is in Submitted state, it cannot be graded by principal
    """
    # Set the assignment to submitted state
    Assignment.query.filter_by(id=3).update({'state': AssignmentStateEnum.SUBMITTED})
    db.session.commit()

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    # Set the assignment to draft state
    Assignment.query.filter_by(id=3).update({'state': AssignmentStateEnum.DRAFT})

    assert response.status_code == 400

def test_grade_assignment_invalid_grade(client, h_principal):
    """
    failure case: If an invalid grade is provided, it should raise an error
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': 'Z'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['message'] == {'data': {'state': 'GRADED'}, 'message': "{'grade': ['Invalid enum member Z']}"}

def test_grade_assignment_no_grade(client, h_principal):
    """
    failure case: If no grade is provided, it should raise an error
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['message'] == {'data': {'state': 'GRADED'}, 'message': "{'grade': ['Missing data for required field.']}"}

def test_grade_non_existent_assignment(client, h_principal):
    """
    failure case: If the assignment does not exist, it should raise an error
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 100,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404
    assert response.json['message'] == 'No assignment with this id was found'

def test_no_header(client):
    
    h_principal = {
        'X-Principal': json.dumps({
            'principal_id': 3,
            'user_id': 5
        })
    }

    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['message'] == 'Principal not found'

def test_invalid_request_body_regrade(client, h_principal):
    """
    failure case: If an invalid request body is provided, it should raise an error
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'teacher_id': 1,
            'grade': 'A'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['message'] ==  {'data': {'state': 'GRADED'}, 'message': "{'id': ['Missing data for required field.']}"}

def test_principal_model():
    
    principal = Principal()
    assert principal.__repr__() == '<Principal None>'