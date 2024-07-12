def test_grade_assignment_2(client, h_grading_by_teacher_2):
    response = client.post('/teacher/assignments/grade',
                           json={
                               "id": 2,
                               "grade": 'A'
                           },
                           headers=h_grading_by_teacher_2)

    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'


def test_grade_assignment_3(client, h_grading_by_teacher_2):
    response = client.post('/teacher/assignments/grade',
                           json={
                               "id": 3,
                               "grade": 'A'
                           },
                           headers=h_grading_by_teacher_2)

    assert response.status_code == 200
    assert response.json['data']['state'] == 'GRADED'
    assert response.json['data']['grade'] == 'A'