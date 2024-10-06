def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400

def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_submit_assignment_bad_teacher(client, h_student_1):
    """
    failure case: teacher does not exist
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 100000
        })

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

import pytest
from core.models.assignments import AssignmentStateEnum

def test_post_new_assignment(client, h_student_1):
    """Test creating a new assignment"""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'New assignment content'
        })

    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == 'New assignment content'
    assert data['state'] == AssignmentStateEnum.DRAFT.value
    assert data['student_id'] == 1

def test_edit_existing_assignment(client, h_student_1):
    """Test editing an existing assignment"""
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'Original content'
        })
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']

    edit_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'content': 'Updated content'
        })

    assert edit_response.status_code == 200
    data = edit_response.json['data']
    assert data['id'] == assignment_id
    assert data['content'] == 'Updated content'
    assert data['state'] == AssignmentStateEnum.DRAFT.value


@pytest.mark.parametrize("invalid_payload", [
    {},
    {'id': 2},
    {'teacher_id': 1},
    {'id': 'not_an_int', 'teacher_id': 1},
    {'id': 2, 'teacher_id': 'not_an_int'},
])
def test_submit_assignment_invalid_payload(client, h_student_1, invalid_payload):
    """Test submitting an assignment with invalid payload"""
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json=invalid_payload)

    assert response.status_code == 400
    assert 'error' in response.json

def test_submit_assignment_wrong_student(client, h_student_2):
    """Test submitting an assignment that belongs to a different student"""
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 2,
            'teacher_id': 1
        })

    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
