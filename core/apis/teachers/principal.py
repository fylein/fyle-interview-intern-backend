from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.teachers import Teacher

from .schema import TeacherSchema
principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of Teachers"""
    all_the_teachers = Teacher.all_teachers()
    all_the_teachers_dump = TeacherSchema().dump(all_the_teachers, many=True)
    return APIResponse.respond(data=all_the_teachers_dump)
