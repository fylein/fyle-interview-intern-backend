from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.libs.exceptions import FyleError

from core.apis.assignments.schema import AssignmentSchema

principal_teacher_resources = Blueprint("principal_teacher_resources", __name__)


@principal_teacher_resources.route("/", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all()
    teachers_dump = AssignmentSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
