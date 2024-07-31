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


def test_grade_assignment_draft_assignment(client, h_principal,h_student_1):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    content = 'Test Assignment'
    create_response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': content}
    )
    assert create_response.status_code == 200
    assignment_id = create_response.json['data']['id']

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
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

def test_get_teachers_wrong_role(client, h_principal2):
    # Assuming h_teacher provides headers for a teacher (non-principal) user
    response = client.get(
        '/principal/teachers',
        headers=h_principal2
    )

    assert response.status_code == 401  

def test_list_teachers_unauthorized(client, h_student_1):
    response = client.get(
        '/principal/teachers',
        headers=h_student_1
    )

    assert response.status_code == 403

def test_list_teachers_principal(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200
    data = response.json['data']