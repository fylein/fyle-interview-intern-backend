from core.models.assignments import AssignmentStateEnum, GradeEnum
from core import db
from core.models.assignments import Assignment

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal, db_session):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    # Make the assignment draft
    Assignment.query.filter_by(id=5).update({'state': AssignmentStateEnum.DRAFT})
    db.session.commit()
    
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    assert response.status_code == 400


def test_grade_assignment(client, h_principal, h_student_2, h_teacher_2, db_session):
    
    # Set the assignment to submitted state
    response = client.post(
        '/student/assignments/submit',
        json={
            'id': 4,
            'teacher_id': 2
        },
        headers=h_student_2
    )

    # Grade the assignment
    response = client.post(
        "/teacher/assignments/grade",
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        },
        headers=h_teacher_2
    )

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    # Set the assignment to draft state
    Assignment.query.filter_by(id=4).update({'state': AssignmentStateEnum.DRAFT})
    db.session.commit()

    assert response.status_code == 200



def test_regrade_assignment(client, h_principal, db_session):

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_list_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200
