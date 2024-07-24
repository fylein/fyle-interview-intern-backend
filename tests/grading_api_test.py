from core.models.assignments import AssignmentStateEnum, GradeEnum,Assignment

def test_grade_assignment_success(client, h_teacher_1):
    """Test grading a submitted assignment successfully."""
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

    assert data['error'] == 'FyleError'

def test_grade_assignment_invalid_state(client, h_teacher_1):
  
    """Test grading an assignment that is not in SUBMITTED state."""
    response = client.post(
        'teacher/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.B.value
        },
        headers=h_teacher_1,
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error']=='FyleError'

def test_grade_assignment_not_found(client, h_teacher_1):
    """Test grading a non-existent assignment."""
    response = client.post(
        'teacher/assignments/grade',
        json={
            'id': 999,
            'grade': GradeEnum.D.value
        },
        headers=h_teacher_1,
    )
    
    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment_missing_grade(client, h_teacher_1):
    """Test grading an assignment without specifying a grade."""
    response = client.post(
        'teacher/assignments/grade',
        json={
            'id': 2
        },
        headers=h_teacher_1,
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error']=='ValidationError'
    
def test_grade_assignment_unauthorized(client):
    """Test grading an assignment without authorization."""
    response = client.post(
        'teacher/assignments/grade',
        json={
            'id': 2,
            'grade': GradeEnum.A.value
        }
    )
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data['error']=='FyleError'