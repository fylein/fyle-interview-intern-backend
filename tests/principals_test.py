from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
import pytest
from core import db, app

@pytest.fixture
def setup_assignment_draft():
    """Fixture to set up an assignment in Draft state."""
    with app.app_context():
        # Create an assignment in Draft state
        db.session.query(Assignment).filter_by(id=5).delete()
        db.session.commit()
        assignment = Assignment(id=5, state=AssignmentStateEnum.DRAFT, student_id=1)
        db.session.add(assignment)
        db.session.commit()
    yield assignment# This allows the test to run after setup
    # Optionally, you can clean up after the test if necessary
    with app.app_context():
        db.session.query(Assignment).filter_by(id=5).delete()
        db.session.commit()
        
def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal, setup_assignment_draft):
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

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
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

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
