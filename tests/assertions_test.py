def test_assert_auth(client):
    response = client.get("/principal/assignments")
    assert response.status_code == 401


def test_assert_true(client, h_student_invalid):
    response = client.get("/student/assignments", headers=h_student_invalid)
    assert response.status_code == 403
