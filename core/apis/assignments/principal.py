from flask import Blueprint
from core import db
from core.apis import decorators
from core.libs import helpers, assertions
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_graded_submissions(p):
    """Return all graded submissions"""
    graded_assignments = Assignment.query.filter_by(state="GRADED").all()
    graded_assignments_dump = AssignmentSchema().dump(graded_assignments, many=True)
    return APIResponse.respond(data=graded_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_assignment_payload['id'])
    if not assignment:
        return APIResponse.respond_error(f"Assignment with ID {grade_assignment_payload['id']} not found", status_code=404)
    assignment.grade = grade_assignment_payload['grade']
    assignment.state = 'GRADED'
    assignment.updated_at = helpers.get_utc_now() 
    db.session.commit()
    updated_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=updated_assignment_dump)
