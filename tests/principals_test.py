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

def test_get_assignments_bad_principal(client, h_principal_bad):
    response = client.get(
        '/principal/assignments',
        headers=h_principal_bad
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal id does not exist'


def test_get_all_teachers_bad_principal(client, h_principal_bad):
    response = client.get(
        '/principal/teachers',
        headers=h_principal_bad
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal id does not exist'

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


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
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

def get_all_teachers(client, h_principal):
    response = client.post(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200
    response = response.json['data']
    for teacher in response:
        assert teacher['user_id'] in [3, 4]

def test_grade_assignment_bad_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            "id": 1,
            "grade": "AB"
        },
        headers=h_principal
    )
    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


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
