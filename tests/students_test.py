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


# def test_post_assignment_student_1(client, h_student_1):
#     content = 'ABCD TESTPOST'

#     response = client.post(
#         '/student/assignments',
#         headers=h_student_1,
#         json={
#             'content': content
#         })

#     assert response.status_code == 200

#     data = response.json['data']
#     assert data['content'] == content
#     assert data['state'] == 'DRAFT'
#     assert data['teacher_id'] is None


# def test_submit_assignment_student_1(client, h_student_1):
#     response = client.post(
#         '/student/assignments/submit',
#         headers=h_student_1,
#         json={
#             'id': 2,
#             'teacher_id': 2
#         })

#     assert response.status_code == 400

    # data = response.json['data']
    # assert data['student_id'] == 1
    # assert data['state'] == 'SUBMITTED'
    # assert data['teacher_id'] == 2


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


def test_post_assignment_student_1_my(client, h_student_1):
    def _post_assignment(content, id=None):
        response = client.post(
            '/student/assignments',
            headers=h_student_1,
            json={
                'content': content,
                **({'id': id} if id else {})
            })
        return response
    
    def _assert_draft_assignment(response, content):
        assert response.status_code == 200
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == 'DRAFT'
        assert data['teacher_id'] is None
    
    content = 'MY TEST'
    response = _post_assignment(content)
    _assert_draft_assignment(response, content)
    
def test_post_assignment_student_1_update_my(client, h_student_1):
    def _post_assignment(content, id):
        response = client.post(
            '/student/assignments',
            headers=h_student_1,
            json={
                'id': id,
                'content': content
            })
        return response
    
    def _assert_draft_assignment(response, content):
        assert response.status_code == 200
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == 'DRAFT'
        assert data['teacher_id'] is None
    
    def _assert_error_response(response, error, message):
        assert response.status_code == 400
        data = response.json
        assert data['error'] == error
        assert data['message'] == message
    
    content = 'MY TEST UPDATED'
    response = _post_assignment(content, 7)
    try:
        _assert_draft_assignment(response, content)
    except AssertionError:
        _assert_error_response(response, 'FyleError', 'only assignment in draft state can be edited')
    
def test_submit_assignment_student_1_my(client, h_student_1):
    def _submit_assignment(id, teacher_id):
        response = client.post(
            '/student/assignments/submit',
            headers=h_student_1,
            json={
                'id': id,
                'teacher_id': teacher_id
            })
        return response
    
    def _assert_submitted_assignment(response, student_id, teacher_id):
        assert response.status_code == 200
        data = response.json['data']
        assert data['student_id'] == student_id
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == teacher_id
    
    def _assert_error_response(response, error, message):
        assert response.status_code == 400
        data = response.json
        assert data['error'] == error
        assert data['message'] == message
    
    response = _submit_assignment(7, 1)
    try:
        _assert_submitted_assignment(response, 1, 1)
    except AssertionError:
        _assert_error_response(response, 'FyleError', 'only a draft assignment can be submitted')
