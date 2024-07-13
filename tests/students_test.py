# /tests/students_test.py

# Get all the assignments of student 1
def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1

# Get all the assignments of student 2
def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

# post a new assignment of student 1 where the content in null
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

# post a new assignment of student 1 where the content in not null
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

# edit an assignment of student 1
def test_post_edit_assignment_student_2(client, h_student_1):
    content = 'THESIS T1 EDITTED'
    id = 2

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": id,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['id'] == id
    assert data['content'] == content
    assert data['state'] == 'DRAFT'

# edit an assignment of student 2 where the assignment is already submitted
def test_post_edit_assignment_student_1_graded(client, h_student_2):
    """
    failure case: only assignment in draft state can be edited
    """
    content = 'THESIS T2 EDITTED'
    id = 4

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            "id": id,
            'content': content
        })

    assert response.status_code == 400

# edit an assignment of student 2 where the content in not null but invalid assignment id
# def test_post_edit_assignment_student_1_invalid_assignment(client, h_student_1):
#     """
#     failure case: No assignment with this id was found
#     """
#     id = 50
#     content = 'EDIT NON_EXISTENT ASSIGNMENT'

#     response = client.post(
#         '/student/assignments',
#         headers=h_student_1,
#         json={
#             "id": id,
#             'content': content
#         })

#     assert response.status_code == 404

# submit an assignment of student 1
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

# resubmit an assignment which was already submitted
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