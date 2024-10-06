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


    # print(response.json)

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_3):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_3,
        json={
            'id': 4,
            'teacher_id': 2
        })
    
    # print(response.json)

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 2
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    
    assert response.status_code == 400

    error_response = response.json
    assert error_response["message"] == '400 Bad Request: Only a draft assignment can be submitted'


def test_submit_assignment_not_found(client, h_student_1):
    """
    Test case for submitting an assignment that does not exist.
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            "id": 99999,  
            "teacher_id": 1
        }
    )
    assert response.json['message'] == '400 Bad Request: Assignment not found'

def test_submit_assignment_non_draft(client, h_student_1):
    """
    Test case for trying to submit an assignment that is not in draft state.
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            "id": 1,  
            "teacher_id": 1
        }
    )

    assert response.json['message'] == '400 Bad Request: Only a draft assignment can be submitted'

def test_upsert_assignment_invalid_payload(client, h_student_1):
    """
    Test case for an invalid payload when creating or editing an assignment.
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "title": "",  
            "description": "This is an assignment."
        }
    )

    assert response.status_code == 400  
    assert response.json['error'] == 'ValidationError'  


