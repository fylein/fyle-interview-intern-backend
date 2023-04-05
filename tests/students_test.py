from core.models.students import Student


def test_student_repr():
    student = Student(id=123)
    expected_output = "<Student 123>"
    assert repr(student) == expected_output


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


def test_assingment_resubmitt_error(client, h_student_1):
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


def test_post_assignment_missing_content(client, h_student_1):
    '''
    failure case: content is missing 
    '''
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={}
    )

    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'
    assert 'content' in response.json['message']


def test_submit_assignment_invalid_teacher(client, h_student_1):
    '''
    Failure case : teacher_id is invalid
    '''
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 'invalid'
        }
    )

    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'
    assert 'teacher_id' in response.json['message']

def test_submit_assignment_wrong_student(client, h_student_2):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 401
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'This assignment belongs to some other student'


def test_assignment_principal_not_found(client):
    response = client.post(
        '/student/assignments',
        json={}
    )

    assert response.status_code == 401
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'principal not found'
   
   




    
