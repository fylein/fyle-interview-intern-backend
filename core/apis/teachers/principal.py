from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from .schema import Teacher, TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    principal_teachers = Teacher.query.all()
    principal_assignments_dump = TeacherSchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=principal_assignments_dump)