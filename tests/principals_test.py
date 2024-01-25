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


# Change : Test case for list of teachers
def test_list_teachers(client,h_principal):

    response = client.get(
        '/principal/teachers',
        headers=h_principal,
    )
    data = response.json['data']

    assert response.status_code == 200 
    print(data)
    teacher_ids=[1,2]
    assert data[0]['id'] in teacher_ids
    assert data[1]['id'] in teacher_ids

# Change : Test case for authentication

def test_principal_authentication(client):
    response = client.get(
        '/principal/teachers',
        headers=None,
    )
    assert response.status_code == 401
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal not found'

# Change : Test case for requester type

def test_requester_type(client, h_student_1):
    response = client.get(
        '/principal/teachers',
        headers=h_student_1,
    )
    assert response.status_code == 403
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'requester should be a principal'