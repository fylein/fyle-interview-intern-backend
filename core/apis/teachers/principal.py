from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import TeacherSchema


principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)
#get/principal/teachers

@principal_teachers_resources.route("/teachers", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_assignment_by_teacher(p):
    """return list of all the teachers"""
    teachers=Teacher.filter()
    all_teachers_dump=TeacherSchema().dump(teachers,many=True)
    return APIResponse.respond(data=all_teachers_dump)


