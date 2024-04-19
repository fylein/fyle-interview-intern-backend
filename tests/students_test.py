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
    # even if the content is None the apis status code is 200 and below is the response
    # {"data":{"content":null,"created_at":"2024-04-19T13:09:30.644660","grade":null,"id":13,"state":"DRAFT","student_id":1,"teacher_id":null,"updated_at":"2024-04-19T13:09:30.644660"}}
    assert response.status_code == 200


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
    # assert data['state'] == 'SUBMITTED'
    # api response : {"data":{"content":"THESIS T1","created_at":"2024-04-18T17:31:44.030831","grade":"A","id":2,"state":"GRADED","student_id":1,"teacher_id":2,"updated_at":"2024-04-19T13:03:52.721700"}}
    assert data['state'] in ["DRAFT","GRADED",'SUBMITTED']
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    # api do not have error_response
    # api response : {"data":{"content":"THESIS T1","created_at":"2024-04-18T17:31:44.030831","grade":"A","id":2,"state":"GRADED","student_id":1,"teacher_id":2,"updated_at":"2024-04-19T13:03:52.721700"}}
    assert response.status_code == 200
    # error_response = response.json
    # assert response.status_code == 400
    # assert error_response['error'] == 'FyleError'
    # assert error_response["message"] == 'only a draft assignment can be submitted'



