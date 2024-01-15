from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema

principal_teacher_resources = Blueprint('principal_teacher_resources', __name__)

@principal_teacher_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):   
    '''
    List all the teachers

    headers:
    X-Principal: {"user_id":5, "principal_id":1}


    response:
    {
        "data": [
            {
                "created_at": "2024-01-08T07:58:53.131970",
                "id": 1,
                "updated_at": "2024-01-08T07:58:53.131972",
                "user_id": 3
            }
        ]
    }
    '''

    teachers = Teacher.get_all_teachers(principal_id=p.principal_id, user_id=p.user_id)
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
    