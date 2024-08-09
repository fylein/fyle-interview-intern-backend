from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

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

    assert response.status_code == 400



def test_grade_assignment(client, h_principal,setup_assignment):
    """Test grading an assignment"""
    assignment_id = setup_assignment

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    # Print the response content for debugging
    print("Response Status Code (Grade Assignment):", response.status_code)
    print("Response Content (Grade Assignment):", response.json())

    assert response.status_code == 200, f"Failed to grade assignment: {response.json()}"
    assert response.json()['data']['state'] == AssignmentStateEnum.GRADED.value, \
        f"Assignment state should be 'GRADED': {response.json()}"
    assert response.json()['data']['grade'] == GradeEnum.C.value, \
        f"Assignment grade should be '{GradeEnum.C.value}': {response.json()}"

def test_regrade_assignment(client, h_principal, setup_assignment):
    """Test regrading an assignment"""
    assignment_id = setup_assignment

    # First, ensure the assignment is graded
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )
    assert response.status_code == 200, f"Failed to initially grade assignment: {response.json()}"
    assert response.json()['data']['state'] == AssignmentStateEnum.GRADED.value, \
        f"Assignment state should be 'GRADED': {response.json()}"
    assert response.json()['data']['grade'] == GradeEnum.C.value, \
        f"Assignment grade should be '{GradeEnum.C.value}': {response.json()}"

    # Regrade the assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )
    # Print the response content for debugging
    print("Response Status Code (Regrade Assignment):", response.status_code)
    print("Response Content (Regrade Assignment):", response.json())

    assert response.status_code == 200, f"Failed to regrade assignment: {response.json()}"
    assert response.json()['data']['state'] == AssignmentStateEnum.GRADED.value,  f"Assignment state should be 'GRADED': {response.json()}"
    assert response.json()['data']['grade'] == GradeEnum.B.value, \
        f"Assignment grade should be '{GradeEnum.B.value}': {response.json()}"
