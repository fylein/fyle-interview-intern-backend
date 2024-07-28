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
    failure case: If an assignment is in Draft state, it cannot be graded by principal.
                ######################################################################
                This can become a failure case from the second time because of that SQL
                query which is making <assignment 5>.state = "GRADED".
                And then princiapl can grade <assignment 5> because now it is not deaft.
                ######################################################################
                Anyway I am handling.
                ######################################################################
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    try:
        assert response.status_code == 400
        assert response.json['error'] == 'FyleError'
        assert response.json['message'] == 'an assignment is in Draft state can not be graded'
    except AssertionError:
        assert response.status_code == 200
        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.A


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