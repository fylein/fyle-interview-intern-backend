from flask import Blueprint
from core.apis import decorators
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentSubmitSchema
from core.apis.responses import APIResponse

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


@principal_assignments_resources.route(
    "/assignments", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments = Assignment.get_assignments_by_principal(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(
        principal_assignments, many=True
    )
    return APIResponse.respond(data=principal_assignments_dump)
