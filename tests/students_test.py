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

def test_get_assignment_not_found(client, h_student_1):
    # Assume assignment with id 9999 doesn't exist
    non_existent_id = 9999
    
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
              'id': non_existent_id,
              'content': 'some updated text'
        })

    assert response.status_code == 404

def test_edit_assignment_not_in_draft_state(client, h_student_1):
    
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
              'id': 1,
              'content': 'some updated text'
        })

    assert response.status_code == 400

def test_no_such_api(client, h_student_1):
    """Test that accessing a non-existent API endpoint results in a 404 error with the 'No such api' message"""

    # Simulate a request to a non-existent endpoint
    response = client.get(
        '/unsupported',
        headers=h_student_1
    )

    # Check that the status code is 404 Not Found
    assert response.status_code == 404