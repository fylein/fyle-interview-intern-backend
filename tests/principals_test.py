from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get("/principal/assignments", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["state"] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        "/principal/assignments/grade", json={"id": 5, "grade": GradeEnum.A.value}, headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        "/principal/assignments/grade", json={"id": 3, "grade": GradeEnum.C.value}, headers=h_principal
    )

    assert response.status_code == 200
    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        "/principal/assignments/grade", json={"id": 3, "grade": GradeEnum.B.value}, headers=h_principal
    )

    assert response.status_code == 200
    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.B


def test_get_teachers(client, h_principal):
    response = client.get("/principal/teachers", headers=h_principal)

    assert response.status_code == 200


def test_invalid_grade_assignment_for_principal(client, h_principal):
    response = client.post("/principal/assignments/grade", json={"id": 5, "grade": "F"}, headers=h_principal)

    error_response = response.json
    assert response.status_code == 400
    assert error_response["message"] == {"grade": ["Invalid enum member F"]}
