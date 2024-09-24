from flask import Blueprint, jsonify, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema, AssignmentGradeSchema  # Import your schema
from core.libs import assertions

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns a list of all submitted and graded assignments."""
    assignments = Assignment.get_assignments_by_principal()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assertions.assert_found(assignment, 'No assignment with this id was found')
    
    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond(
            message='Assignment in draft state cannot be graded',
            status_code=400
        )

    assignment.grade = GradeEnum(grade_assignment_payload.grade)
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)

