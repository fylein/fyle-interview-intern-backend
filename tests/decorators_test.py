def test_unauthorized_exception(client):
    """
    failure case: If X-Principal header is not present
    """
    response = client.get(
        "/student/assignments",
    )

    assert response.status_code == 401


def test_forbidden_exception_principal_route(client, h_invalid_header):
    """
    failure case: Non principal user cannot access principal apis
    """
    response = client.get("/principal/teachers", headers=h_invalid_header)

    assert response.status_code == 403


def test_forbidden_exception_student_route(client, h_invalid_header):
    """
    failure case: Non principal user cannot access principal apis
    """
    response = client.get("/student/assignments", headers=h_invalid_header)

    assert response.status_code == 403


def test_forbidden_exception_teacher_route(client, h_principal):
    """
    failure case: Non principal user cannot access principal apis
    """
    response = client.get("/teacher/assignments", headers=h_principal)

    assert response.status_code == 403
