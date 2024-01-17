from core.models.assignments import Assignment


def test_assignment_repr():
    assignment = Assignment(id=123)

    result = repr(assignment)

    assert result == "<Assignment 123>"


def test_invalid_edit_assignment_student_1(client, h_student_1):
    content = "ABCD TESTPOST"

    response = client.post("/student/assignments", headers=h_student_1, json={"content": content, "id": 6})

    error_response = response.json
    assert response.status_code == 404
    assert error_response["message"] == "No assignment with this id was found"


def test_valid_edit_assignment_student_1(client, h_student_1):
    content = "ABCD TESTPOST"

    response = client.post("/student/assignments", headers=h_student_1, json={"content": content, "id": 5})

    assert response.status_code == 200
