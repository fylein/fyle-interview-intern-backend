def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    has_teacher_1 = False
    for assignment in data:
        if assignment['teacher_id'] == 1:
            has_teacher_1 = True
            break  

    assert has_teacher_1  


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200
    
    assert 'data' in response.json

    teacher_assignments = [assignment for assignment in response.json['data'] if assignment['teacher_id'] == 2]
    assert teacher_assignments

    for assignment in teacher_assignments:
        assert 'teacher_id' in assignment
        assert assignment['teacher_id'] == 2
        assert 'state' in assignment
        assert assignment['state'] in ['SUBMITTED', 'GRADED', 'DRAFT']

    

def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'Only submitted assignments can be graded.'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'Assignment not found.'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400

    data = response.json

    assert data['error'] == 'Only submitted assignments can be graded.'




def test_grade_assignment_malformed_payload(client, h_teacher_1):
    """
    Failure case: Test the API with a malformed payload.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "grade": "A"  
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'  



def test_grade_assignment_invalid_payload(client, h_teacher_1):
    response = client.post('/teacher/assignments/grade', headers=h_teacher_1, json={"id": 1})
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'


def test_list_assignments_with_different_states(client, h_teacher_1):
    response = client.get('/teacher/assignments', headers=h_teacher_1)
    assert response.status_code == 200
    for assignment in response.json['data']:
        assert assignment['state'] in ['SUBMITTED', 'GRADED', 'DRAFT']  # Validate states

def test_grade_assignment_large_grade(client, h_teacher_1):
    """
    Test case for grading an assignment with a grade value that exceeds normal limits.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,  
            "grade": 101  
        }
    )

    assert response.status_code == 400  
    assert response.json['error'] == 'ValidationError'  


