from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get("/principal/assignments", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["state"] in [
            AssignmentStateEnum.SUBMITTED,
            AssignmentStateEnum.GRADED,
        ]


def test_get_teachers_list(client, h_principal):
    response = client.get("/principal/teachers", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for teachers in data:
        assert teachers["id"] in [1, 2]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 5, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.C.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.C


def test_grade_invalid_assignment_id(client, h_principal):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 999, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 404
    data = response.json

    assert data["error"] == "FyleError"


def test_grade_assignment_missing_payload(client, h_principal):
    """
    failure case: If payload is missing and throw 404
    """
    response = client.post(
        "/principal/assignments/grade",
        headers=h_principal,
    )

    assert response.status_code == 400
    data = response.json

    assert data["error"] == "ValidationError"


def test_regrade_assignment(client, h_principal):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.B.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.B
