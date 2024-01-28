from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Teacher
from .schema import TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

# Change API for principal/teacher is created

@principal_teachers_resources.route('', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_of_teachers(p):
    """Returns list of teachers"""
    list_of_teachers = Teacher.get_all()
    list_of_teachers_dump = TeacherSchema().dump(list_of_teachers, many=True)
    return APIResponse.respond(data=list_of_teachers_dump)