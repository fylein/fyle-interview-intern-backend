from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.principals import Principal
from core.libs import helpers, assertions


from .schema import TeacherSchema
principal_resources = Blueprint('principal_resources', __name__)


@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    if Principal.get_by_id(p.principal_id):
        teachers = Teacher.get_teachers()
        teachers_dump = TeacherSchema().dump(teachers, many=True)
        return APIResponse.respond(data=teachers_dump)