def test_get_assignments_student_1(client, h_student_1):
    """Test retrieving assignments for student 1."""
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """Test retrieving assignments for student 2."""
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """Test posting an assignment with null content."""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400

def test_post_assignment_content(client, h_student_1):
    """Test posting an assignment with  content."""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'abcd'
        })

    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == 'abcd'


def test_post_assignment_student_1(client, h_student_1):
    """Test posting an assignment for student 1."""
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


def test_submit_assignment_assignment_not_found(client, h_student_1):
    """Test submitting an assignment that doesn't exist."""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 1000,  # Assuming 999 is a non-existing assignment ID
            'content': "some updated text"
        })
    print(response)
    assert response.status_code == 404

    error_response = response.json
    assert error_response['error'] == 'FyleError'

def test_submit_assignment_student_1(client, h_student_1):
    """Test submitting an assignment for student 1."""
    # Create a new assignment for the test
    response_create = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'New Assignment'}
    )
    new_assignment_id = response_create.json['data']['id']

    # Submit the newly created assignment
    response_submit = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={'id': new_assignment_id, 'teacher_id': 2}
    )

    assert response_submit.status_code == 200

    data = response_submit.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """Test resubmitting an already submitted assignment."""
    # Assuming that there is an assignment with id=2 in a submitted state
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
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


def test_assignment_upsert_new(client,h_student_1):
    
    new_content = 'New Content'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': new_content}
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == new_content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
def test_assignment_upsert_drafted(client,h_student_1):
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'abcd'
        })
    data = response.json['data']
    _id = data['id']
    new_content="abcd"
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'id':_id,
            'content': new_content}
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == new_content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

