import json
from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_grade_assignment_draft_assignment_principal(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment_principal(client, h_principal):
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


def test_regrade_assignment_principal(client, h_principal):
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


def test_grade_nonexistent_assignment_principal(client, h_principal):
    """
    Test attempting to grade a nonexistent assignment.
    """
    non_existent_assignment_id = 999999  # Assume this ID does not exist
    grade_response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': non_existent_assignment_id,
            'grade': 'B'
        }
    )
    assert grade_response.status_code == 404
    data = grade_response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_grade_principal(client, h_principal):
    """
    Test grading an assignment with an invalid grade.
    """

    # Attempt to grade the assignment with an invalid grade
    invalid_grade_response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': 4,
            'grade': 'Z'  # Assume 'Z' is an invalid grade
        }
    )
    assert invalid_grade_response.status_code == 400
    error_response = invalid_grade_response.json

    assert error_response['error'] == 'ValidationError'


# Add teacher grading tests


def test_grade_assignment_cross_teacher(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "B"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade_teacher(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "CD"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment_teacher(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "B"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment_teacher(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1, json={
            "id": 2,
            "grade": "B"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
