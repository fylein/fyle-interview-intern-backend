from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentSubmitSchema

student_assignments_resources = Blueprint('student_assignments_resources', __name__)

@student_assignments_resources.route('/assignments/<int:assignment_id>', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_assignment(p, assignment_id):
    """Returns a specific assignment"""
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error(message='Assignment not found', status_code=404)
    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)

@student_assignments_resources.route('/assignments/<int:assignment_id>', methods=['PUT'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def update_assignment(p, assignment_id, incoming_payload):
    """Update an assignment"""
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error(message='Assignment not found', status_code=404)

    updated_assignment = AssignmentSchema().load(incoming_payload, instance=assignment, partial=True)
    db.session.commit()
    updated_assignment_dump = AssignmentSchema().dump(updated_assignment)
    return APIResponse.respond(data=updated_assignment_dump)

@student_assignments_resources.route('/assignments/<int:assignment_id>', methods=['DELETE'], strict_slashes=False)
@decorators.authenticate_principal
def delete_assignment(p, assignment_id):
    """Delete an assignment"""
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error(message='Assignment not found', status_code=404)

    db.session.delete(assignment)
    db.session.commit()
    return APIResponse.respond(message='Assignment deleted successfully')
