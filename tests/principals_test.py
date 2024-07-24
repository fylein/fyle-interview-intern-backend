from core.models.assignments import AssignmentStateEnum, GradeEnum,Assignment


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
    draft_assignment = Assignment.query.filter_by(state=AssignmentStateEnum.DRAFT).first()
    if draft_assignment is not None:
        test_id=draft_assignment.id
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': test_id,
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
def test_grade_non_existant_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4000,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 404
def test_bad_grade_assignment(client, h_principal):
    """
    failure case: If an assignment is graded a grade that is not in GradeEnum range
    """
    draft_assignment = Assignment.query.filter_by(state=AssignmentStateEnum.DRAFT).first()
    if draft_assignment is not None:
        test_id=draft_assignment.id
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': test_id,
                'grade': "AB"
            },
            headers=h_principal
        )

        assert response.status_code == 400