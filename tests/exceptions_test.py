def test_exceptions_to_dict(client, h_student_1):
    response = client.get("/student/test", headers=h_student_1)

    assert response.status_code == 400
