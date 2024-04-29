from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_assignments(p):
    """Returns list of submitted and graded assignments"""
    graded_assignments = Assignment.query.filter(
        (Assignment.state == AssignmentStateEnum.GRADED) | (Assignment.state == AssignmentStateEnum.SUBMITTED)
    ).all()
    assignment_schema = AssignmentSchema(many=True)

    return APIResponse.respond(
        data=assignment_schema.dump(graded_assignments)
    )

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
  
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
