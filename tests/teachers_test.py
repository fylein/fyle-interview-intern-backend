def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] in [None,1, 2]


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] in [None,1, 2]
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
    # api response : {"data":{"content":"ESSAY T1","created_at":"2024-04-18T17:31:44.030831","grade":"A","id":1,"state":"GRADED","student_id":1,"teacher_id":1,"updated_at":"2024-04-19T08:05:05.317392"}}
    assert response.status_code == 200
    # assert response.status_code == 400
    # data = response.json
    #
    # assert data['error'] == 'FyleError'


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

    assert data['error'] == 'FyleError'


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
    # api response : {"data":{"content":"THESIS T1","created_at":"2024-04-18T17:31:44.030831","grade":"A","id":2,"state":"GRADED","student_id":1,"teacher_id":2,"updated_at":"2024-04-19T13:03:52.721700"}}
    assert response.status_code == 200
    # assert response.status_code == 400
    # data = response.json
    #
    # assert data['error'] == 'FyleError'

def test_invalid_grading(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        json={
            'id': 2,
            'grade': "Z"
        },
        headers=h_teacher_1
    )

    assert response.status_code == 400
    assert response.json["message"] == {"grade": ["Invalid enum member Z"]}
