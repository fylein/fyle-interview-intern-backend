from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'],strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(principal):
    """List all submitted and graded assignments"""
    assignments = Assignment.query.filter((Assignment.state == 'SUBMITTED') | (Assignment.state == 'GRADED')).all()
    serialized_assignments = AssignmentSchema(many=True).dump(assignments)
    return APIResponse.respond(data=serialized_assignments)
