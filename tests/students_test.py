from core import db
from sqlalchemy import text
import json
from core.models.students import Student

def test_get_assignments_student_1(client, h_student_1):

    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


# def test_get_assignments_student_2(client, h_student_2):
#     response = client.get(
#         '/student/assignments',
#         headers=h_student_2
#     )

#     assert response.status_code == 200

#     data = response.json['data']
#     for assignment in data:
#         assert assignment['student_id'] == 2


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


def test_post_assignment_student(client, h_student_1):
    """
    Calling upsert without an ID should create a new assignment
    """
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content,
            "teacher_id": 1
        })

    # Remove the assignment created in this test
    db.engine.execute(
        text("DELETE FROM assignments WHERE id = :id"),
        {"id": response.json['data']['id']}
    )
    assert response.status_code == 200
    
    data = response.json['data']
    assert data['content'] == content




def test_submit_assignment_student_2(client, h_student_2):

    # If assignment already exists, set it to DRAFT
    db.engine.execute(
        text("UPDATE assignments SET state = :state WHERE id = :id"),
        {"state": "DRAFT", "id": 4}
    )
    #db.session.commit()

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 4,
            'teacher_id': 2
        })

    # Change the state back to DRAFT
    db.engine.execute(
        text("UPDATE assignments SET state = :state WHERE id = :id"),
        {"state": "DRAFT", "id": 4}
    )
    db.session.commit()
    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 2
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_2):

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

def test_submit_assignment_invalid_student(client, h_student_1):
    
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 4,
            'teacher_id': 2
        })

    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'This assignment belongs to some other student'

def test_submit_graded_assignment(client, h_student_1):
    
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 1,
            'teacher_id': 1
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'only a draft assignment can be submitted'

def test_edit_assignment(client, h_student_2):
    
    content = 'ABCD TESTEDIT'
    # Ensure the assignment is in DRAFT state
    db.engine.execute(
        text("UPDATE assignments SET state = :state WHERE id = :id"),
        {"state": "DRAFT", "id": 3}
    )
    db.session.commit()
    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'id': 3,
            'content': content
        })


    content = db.engine.execute(
        text("SELECT content FROM assignments WHERE id = :id"),
        {"id": 3}
    ).fetchone()[0]

    # Revert the content back to ESSAY T2
    db.engine.execute(
        text("UPDATE assignments SET content = :content WHERE id = :id"),
        {"content": "ESSAY T2", "id": 3}
    )
    db.session.commit()

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content




def test_get_assignments_no_assignments_student_1(client, h_student_1):

    db.engine.execute(
        text("INSERT INTO USERS (id, username, email, created_at, updated_at) VALUES (:id, :name, :email, :created_at, :updated_at)"),
        {"id": 7, "name": "Test User 3", "email": "testuser@fyle.com", "created_at": "2021-01-01 00:00:00", "updated_at": "2021-01-01 00:00:00"}
    )

    db.engine.execute(
        text("INSERT INTO STUDENTS (id, user_id, created_at, updated_at) VALUES (:id, :user_id, :created_at, :updated_at)"),
        {"id": 4, "user_id": 7, "created_at": "2021-01-01 00:00:00", "updated_at": "2021-01-01 00:00:00"}
    )

    '''
    headers = {
        'X-Principal': json.dumps({
            'student_id': 4,
            'user_id': 7
        })
    }
    '''
    header = {
        'X-Principal': json.dumps({
            'student_id': 4,
            'user_id': 7
        })
    }

    response = client.get(
        '/student/assignments',
        headers=header
    )

    # Remove the student created in this test
    db.engine.execute(
        text("DELETE FROM students WHERE id = :id"),
        {"id": 4}
    )

    # Remove the user created in this test
    db.engine.execute(
        text("DELETE FROM users WHERE id = :id"),
        {"id": 7}
    )

    assert response.status_code == 200
    data = response.json['data']
    assert len(data) == 0  

def test_submit_assignment_invalid_teacher(client, h_student_2):

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 4,
            'teacher_id': 999  # Assuming teacher ID 999 doesn't exist
        })

    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'


def test_edit_nonexistent_assignment(client, h_student_1):

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 999,  # Assuming assignment ID 999 doesn't exist
            'content': 'New Content'
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'

def test_upsert_assignment_nonexistent_teacher(client, h_student_1):

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'New Content',
            'teacher_id': 999  # Assuming teacher ID 999 doesn't exist
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'Teacher not found'

def test_upsert_assignment_no_teacher(client, h_student_1):

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'New Content'
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'teacher_id is required'

def test_upsert_assignment_wrong_student(client, h_student_1):
    """
    failure case: This assignment belongs to some other student
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'New Content',
            'teacher_id': 2,
            'id': 3
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'This assignment belongs to some other student'

def test_upsert_assignment_empty_content(client, h_student_1):
    """
    failure case: Content cannot be empty
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': '',
            'teacher_id': 1
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'Content cannot be empty'

def test_submit_assignment_invalid_request_body(client, h_student_1):
    """
    failure case: Invalid request body
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'teacher_id': 1
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == "{'id': ['Missing data for required field.']"

def test_student_model_repr():
    """
    Test Student model __repr__ function
    """

    student = Student()
    student.id = 1
    assert student.__repr__() == '<Student 1>'