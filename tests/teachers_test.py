from core.libs.exceptions import FyleError
from core.models.assignments import AssignmentStateEnum, GradeEnum

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


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

    assert data['error'] == 'ValidationError'


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
    assert data['message'] == 'No assignment with this id was found'


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

    assert response.status_code == FyleError.status_code
    data = response.json

    assert data['error'] == 'FyleError'


def test_get_assignments_teacher_does_not_exist(client, h_teacher_does_not_exist):
    """
    Test case for an invalid teacher
    """
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_does_not_exist
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'Teacher with given id does not exist'


def test_grade_assignment_on_principal_endpoint(client, h_teacher_1):
    """
    failure case: Teachers cannot grade assignment on principal endpoint
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'
    assert data['message'] == 'requester should be a principal'


def test_grade_submitted_assignment(client, h_teacher_2):
    """
    Test case for grading correct assignment
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 3,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json
    assert data['data']['state'] == AssignmentStateEnum.GRADED.value
    assert data['data']['grade'] == GradeEnum.A


def test_regrade_graded_assignment(client, h_teacher_2):
    """
    Test case for regrading an already graded assignment
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 3,
            "grade": "C"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Cannot grade an already graded assignment'