from flask import Blueprint

from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import TeacherSchema
from ..assignments.schema import AssignmentSchema, AssignmentGradeSchema
from ...models.teachers import Teacher

principal_resources = Blueprint('principal_resources', __name__)


@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
