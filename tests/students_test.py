from core import db
from sqlalchemy import text
from tests.conftest import db_session
import json

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


def test_post_assignment_null_content(client, h_student_1, db_session):
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


def test_post_assignment_student_1(client, h_student_1, db_session):
  
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']

    # Remove the assignment created in this test
    db.engine.execute(
        text("DELETE FROM assignments WHERE id = :id"),
        {"id": data['id']}
    )
    
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_2(client, h_student_2, db_session):

    # If assignment already exists, remove it first
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


def test_assignment_resubmit_error(client, h_student_2, db_session):

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

def test_submit_assignment_invalid_teacher(client, h_student_2, db_session):

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 4,
            'teacher_id': 999  # Assuming teacher ID 999 doesn't exist
        })

    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'


def test_edit_nonexistent_assignment(client, h_student_1, db_session):

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 999,  # Assuming assignment ID 999 doesn't exist
            'content': 'New Content'
        })
    
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'