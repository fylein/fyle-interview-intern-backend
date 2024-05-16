from flask import Blueprint

from core.apis import decorators
from core.models.teachers import Teacher
from core.apis.responses import APIResponse
from core.apis.teachers.schema import TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

"""Feat: defining route and endpoint that retrieves list of teachers"""


@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)