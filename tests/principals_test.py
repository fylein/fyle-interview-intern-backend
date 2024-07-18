from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.teachers import Teacher 
from core.models.users import User


def test_user_model_repr():
    user = User(username='testuser', email='testuser@example.com')
    assert repr(user) == '<User \'testuser\'>'


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

def test_list_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    assert len(data) == Teacher.query.count()  
    for teacher in data:
        assert 'id' in teacher
        assert 'user_id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher

        
def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    if response.status_code == 200:
        assert response.json['data']['state'] == AssignmentStateEnum.GRADED
        assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    if response.status_code == 200:
        assert response.json['data']['state'] == AssignmentStateEnum.GRADED
        assert response.json['data']['grade'] == GradeEnum.B

def test_grade_nonexistent_assignment(client, h_principal):
    """
    failure case: Trying to grade an assignment that does not exist
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 9999,  
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404

def test_grade_assignment_without_grade(client, h_principal):
    """
    failure case: Sending a request without a grade
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4  # Assume 4 is an ID of an assignment in SUBMITTED state
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment_invalid_grade(client, h_principal):
    """
    failure case: Sending an invalid grade
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4, 
            'grade': 'InvalidGrade'
        },
        headers=h_principal
    )

    assert response.status_code == 404