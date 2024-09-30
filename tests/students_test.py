def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400

    """These new lines are added here below as per requirement"""
    error_response = response.json
    assert error_response['error'] == 'InvalidRequestError'
    assert error_response['message'] == 'Content cannot be null'


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

    """New attemp happened below"""

def test_submit_non_existent_assignment(client, h_student_1):
    """
    failure case: submitting a non-existent assignment
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 9999,  # Assuming this ID does not exist
            'teacher_id': 2
        }
    )

    assert response.status_code == 404

    # Check for an informative error message
    error_response = response.json
    assert error_response['error'] == 'AssignmentNotFoundError'
    assert error_response['message'] == 'The requested assignment was not found'

def test_submit_assignment_invalid_teacher(client, h_student_1):
    """
    failure case: submitting an assignment to an invalid teacher
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,  # Valid assignment ID
            'teacher_id': 9999  # Assuming this teacher ID does not exist
        }
    )

    assert response.status_code == 400

    # Check for an informative error message
    error_response = response.json
    assert error_response['error'] == 'InvalidTeacherError'
    assert error_response['message'] == 'The teacher ID provided is invalid'


