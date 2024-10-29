from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema
principal_list_teacher_resources = Blueprint('principal_list_teacher_resources', __name__)

@principal_list_teacher_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    teacher_records = Teacher.query.all()
    serialized_teachers = TeacherSchema().dump(teacher_records, many=True)
    return APIResponse.respond(data=serialized_teachers)