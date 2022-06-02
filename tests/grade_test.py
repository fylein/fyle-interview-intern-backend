def test_grade_assigments_teacher_1(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json = {
            "id": 1,
            "grade": "A"
        }
    )
    assert response.status_code == 200
    data = response.json['data']
    assert data['teacher_id']==1
    assert data['id'] == 1
    assert data['grade']=="A"
    assert data['state']=="GRADED"

def test_re_grading_error(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json = {
            "id": 1,
            "grade": "A"
        }
    )
    assert response.status_code == 400
    data = response.json
    assert data['error']=='IntegrityError'
    