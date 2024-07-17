# /tests/students_test.py
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum

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



# post a new assignment
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

# post a new assignment where the content in null
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
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Assignment content cannot be null'



# edit an assignment
def test_post_edit_assignment_student_1(client, h_student_1):
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

# edit an assignment with invalid assignment id
def test_post_edit_invalid_assignment(client, h_student_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": 100000,
            'content': 'EDIT NON_EXISTENT ASSIGNMENT'
        })

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

# edit an assignment of another student
def test_post_edit_wrong_assignment(client, h_student_2):
    """
    failure case: The assignment is not of the requesting student
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            "id": 2, 
            'content': 'STUDENT2 TRYING TO EDIT AN ASSIGNMENT OF STUDENT1'

        })

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'This assignment belongs to another student'

# edit an assignment which was already submitted/graded
def test_post_edit_graded_assignment(client, h_student_2):
    """
    failure case: only assignment in draft state can be edited
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            "id": 4,
            'content': 'THESIS T2 EDITTED'
        })

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Only assignment in draft state can be edited'

# edit an assignment with null content
def test_post_edit_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": 5,
            'content': None
        })

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Assignment content cannot be null'



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

# submit an assignment with invalid assignment id
def test_submit_invalid_assignment(client, h_student_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 5000,
            'teacher_id': 2
        })

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

# submit an assignment of another student
def test_submit_wrong_assignment(client, h_student_2):
    """
    failure case: the assignment is not of the submitting student
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'This assignment belongs to another student'

# resubmit an assignment which was already submitted
def test_assignment_resubmit_error(client, h_student_1):
    """
    failure case: Only Assignments in Draft state can be submitted
    """

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
    assert error_response["message"] == 'This assignment was already submitted, cannot re-submit'

# submit an assignment which has null content
def test_post_submit_empty_assignment(client, h_student_2):
    """
    failure case: assignment content cannot be null
    """
    
    assignment = Assignment(
            student_id=2,
            state=AssignmentStateEnum.DRAFT
        )
    db.session.add(assignment)
    db.session.commit()

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            "id": 7,
            'teacher_id': 1
        })

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Assignment with empty content cannot be submitted'