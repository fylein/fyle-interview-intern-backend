import json
from core.models.users import User


def test_api_without_principal(client):
    response = client.get(
        '/teacher/assignments',
    )

    assert response.status_code == 401
    data = response.json
    data['message'] == 'principal not found'


def test_ready(client):
    response = client.get(
        '/',
    )
    assert response.status_code == 200


def test_http_exception(client, h_teacher_1):
    response = client.get(
        '/assignments/',
        headers=h_teacher_1,
    )

    assert response.status_code == 404
    data = response.json
    data['error'] == 'NotFound'


def test_get_users(h_student_1):
    user_by_id = User.get_by_id(json.loads(h_student_1['X-Principal'])["user_id"])
    user_by_email = User.get_by_email(user_by_id.email)