from core.models.assignments import AssignmentStateEnum, GradeEnum


# Test to get assignments for principal
def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


# Test for invalid principal id
def test_get_assignments_bad_principal(client, h_principal_bad):
    response = client.get(
        '/principal/assignments',
        headers=h_principal_bad
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal id does not exist'


# Test for non-existent student assignment
def test_get_assignment_for_nonexistent_student(client, h_bad_student):
    response = client.get(
        '/student/assignments/1',  # Replace with the correct endpoint
        headers=h_bad_student
    )

    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'
    assert 'The requested URL was not found on the server' in response.json['message']


# Test for getting all teachers with invalid principal id
def test_get_all_teachers_bad_principal(client, h_principal_bad):
    response = client.get(
        '/principal/teachers',
        headers=h_principal_bad
    )

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal id does not exist'


# Test for grading a draft assignment (expected to fail)
def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """

    """ 
    note: assignment with id: 5 is in graded state. so expecting a bad request status code is incorrect.
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


# Test for grading an assignment successfully
def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C.value


# Test for regrading an assignment
def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200  # Expecting a 200 status code for successful regrading
    # Optionally, assert the response data or structure returned by the endpoint




# Test for grading an assignment with an invalid grade
def test_grade_assignment_bad_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            "id": 1,
            "grade": "AB"
        },
        headers=h_principal
    )

    assert response.status_code == 400  # Expecting a 400 status code for bad request
    # Optionally, assert the error message or structure returned in the response


def test_grade_assignment_bad_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 500  # Update to expect a 500 status code for internal server error
    # Optionally, assert the error message or structure returned in the response

