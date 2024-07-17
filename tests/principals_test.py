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
            'id': 124,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 88,
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
            'id': 88,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

    # Feature: Test to retrieve the list of teachers

    def test_get_teachers(client, h_principal):
        response = client.get(
            '/principal/teachers',
            headers=h_principal
        )

        assert response.status_code == 200

    def test_grade_assignment_invalid_grade(client, h_principal):
        """Only valid grades are A,B,C,D"""
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': 'CF'
            },
            headers=h_principal
        )

        assert response.status_code == 400

        def list_all_submitted_and_graded_assignment(client,h_principal):
            response=client.get(
                '/principal/assignments',
                headers=h_principal
            )

            assert response.status_code == 200

        def test_requester_type(client, h_student_1):
            response = client.get(
                '/principal/teachers',
                headers=h_student_1,
            )
            assert response.status_code == 403
            assert response.json['error'] == 'FyleError'
            assert response.json['message'] == 'requester should be a principal'

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
                    'id': 124,
                    'grade': GradeEnum.A.value
                },
                headers=h_principal
            )

            assert response.status_code == 400

        def test_grade_assignment(client, h_principal):
            response = client.post(
                '/principal/assignments/grade',
                json={
                    'id': 88,
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
                    'id': 88,
                    'grade': GradeEnum.B.value
                },
                headers=h_principal
            )

            assert response.status_code == 200

            assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
            assert response.json['data']['grade'] == GradeEnum.B

            # Feature: Test to retrieve the list of teachers

            def test_get_teachers(client, h_principal):
                response = client.get(
                    '/principal/teachers',
                    headers=h_principal
                )

                assert response.status_code == 200

            def test_grade_assignment_invalid_grade(client, h_principal):
                """Only valid grades are A,B,C,D"""
                response = client.post(
                    '/principal/assignments/grade',
                    json={
                        'id': 4,
                        'grade': 'CF'
                    },
                    headers=h_principal
                )

                assert response.status_code == 400


                def test_list_submitted_and_graded_assignments(client, h_principal):
                    response = client.get(
                        '/principal/assignments',
                        headers=h_principal
                    )

                    assert response.status_code == 200

                    data = response.json['data']
                    for assignment in data:
                        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

                def test_requester_type(client, h_student_1):
                    response = client.get(
                        '/principal/teachers',
                        headers=h_student_1,
                    )
                    assert response.status_code == 403
                    assert response.json['error'] == 'FyleError'
                    assert response.json['message'] == 'requester should be a principal'