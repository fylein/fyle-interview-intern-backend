def test_get_assignments_student_1(client, h_student_1):
    """Test that a student can retrieve their own assignments"""
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """Test that a student can retrieve their own assignments"""
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
    Failure case: content cannot be null
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        }
    )

    assert response.status_code == 400

    error_response = response.json
    assert error_response['error'] == 'BadRequest'
    assert error_response['message'] == 'Content cannot be null'


def test_post_assignment_student_1(client, h_student_1):
    """Test posting an assignment for a student"""
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        }
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """Test submitting an assignment"""
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """
    Failure case: Attempting to resubmit an assignment that is already submitted
    """
    # First, submit the assignment to change its state to 'SUBMITTED'
    client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )
    
    # Attempt to resubmit the same assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )
    
    assert response.status_code == 400
    
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Only a draft assignment can be submitted'
