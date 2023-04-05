
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] == 'SUBMITTED'


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] == 'SUBMITTED'




def test_grade_assignment_successful(client, h_teacher_1):
    """
    success case: grade a submitted assignment with valid grade
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json

    assert data['data']['id'] == 1
    assert data['data']['grade'] == "A"
    assert data['data']['state'] == "GRADED"
  



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

    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'
    assert data['message'] == 'Only the assigned teacher can grade this assignment'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should not allow only grades available in enum
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
    assert data['message'] == {'grade': ['Invalid enum member AB']}


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
    assert data['message'] == 'No assignment with this id was found'


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

    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'
    assert data['message'] == 'Only the assigned teacher can grade this assignment'




def test_grade_assignment_graded_assignment(client, h_teacher_1):
    """
    failure case: cannot grade an assignment that has already been graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 3,
            "grade": "B"
        }
    )

    assert response.status_code == 403
    data = response.json

    assert data['error'] == 'FyleError'
    assert data['message'] == 'Only the assigned teacher can grade this assignment'



