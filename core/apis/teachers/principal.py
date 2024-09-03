from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/principal/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""

    all_teachers = Teacher.query.all()
    teachers_schema = TeacherSchema(many=True)
    teachers_dump = teachers_schema.dump(all_teachers)

    return APIResponse.respond(data=teachers_dump)
