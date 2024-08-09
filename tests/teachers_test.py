def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get('/teacher/assignments', headers=h_teacher_1)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1

def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get('/teacher/assignments', headers=h_teacher_2)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

def test_grade_assignment_cross(client, h_teacher_2):
    response = client.post('/teacher/assignments/grade', headers=h_teacher_2, json={"id": 1, "grade": "A"})
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'

def test_grade_assignment_bad_grade(client, h_teacher_1):
    response = client.post('/teacher/assignments/grade', headers=h_teacher_1, json={"id": 1, "grade": "AB"})
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

def test_grade_assignment_bad_assignment(client, h_teacher_1):
    response = client.post('/teacher/assignments/grade', headers=h_teacher_1, json={"id": 100000, "grade": "A"})
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'

def test_grade_assignment_draft_assignment(client, h_teacher_1):
    response = client.post('/teacher/assignments/grade', headers=h_teacher_1, json={"id": 2, "grade": "A"})
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'
