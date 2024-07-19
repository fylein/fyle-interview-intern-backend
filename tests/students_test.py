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
    """
    can be failure case: only a draft assignment can be submitted ( an assignment can't be submitted more than once. )
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    try:
        assert response.status_code == 200
        data = response.json['data']
        assert data['student_id'] == 1
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == 2
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only a draft assignment can be submitted'


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
    content = 'MY TEST'

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



def test_post_assignment_of_student_1_by_studeny_2_my(client, h_student_2):
    content = "STUDENT ID 2 WANTS TO UPDATE STUDENT 1'S MY TEST"

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'id': 7,
            'content': content
        })

    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'This assignment belongs to some other student'


def test_post_assignment_student_1_update_my(client, h_student_1):
    content = 'MY TEST UPDATED'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 7,
            'content': content
        })

    try:    
        assert response.status_code == 200
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == 'DRAFT'
        assert data['teacher_id'] is None
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only assignment in draft state can be edited'


def test_submit_assignment_of_student_1_by_studeny_2_my(client, h_student_2):
    """
    failure case: This assignment belongs to some other student
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 7,
            'teacher_id': 1
        })

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
    assert data['message'] == 'This assignment belongs to some other student'




def test_submit_assignment_student_1_my(client, h_student_1):
    """
    can be failure case: only a draft assignment can be submitted ( an assignment can't be submitted more than once. )
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 7,
            'teacher_id': 1
        })

    try:
        assert response.status_code == 200
        data = response.json['data']
        assert data['student_id'] == 1
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == 1
    except AssertionError:
        assert response.status_code == 400
        data = response.json
        assert data['error'] == 'FyleError'
        assert data['message'] == 'only a draft assignment can be submitted'