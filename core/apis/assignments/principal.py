from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    submitted_graded_assignments = Assignment.get_assignments_by_state([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    submitted_graded_assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=submitted_graded_assignments_dump)

