from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema
from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_assignments(p):
    """List all submitted and graded assignments"""
    # Fetch assignments that are either submitted or graded
    assignments = Assignment.get_submitted_and_graded_assignments()
    
    # Serialize the assignments using AssignmentSchema
    assignments_dump = AssignmentSchema().dump(assignments, many=True)

    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_regrade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.principal_mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
