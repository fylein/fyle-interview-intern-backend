from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from .schema import teachers_details

teachers_resources = Blueprint('teachers_resources', __name__)

@teachers_resources.route('/teachers', methods = ['GET'], strict_slashes = False)
@decorators.authenticate_principal
def list_teachers(p):
    all_teachers_dump = teachers_details().dump(Teacher.get_teachers(), many=True)
    return APIResponse.respond(data = all_teachers_dump)