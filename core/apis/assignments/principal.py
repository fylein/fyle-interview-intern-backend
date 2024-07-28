from sqlalchemy import or_
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_and_graded_assignments(p):
    """Returns list of assignments"""
    principal_assignments = Assignment.filter(or_(Assignment.state == AssignmentStateEnum.GRADED,
                                                  Assignment.state == AssignmentStateEnum.SUBMITTED)).all()

    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment_by_principal(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    print(graded_assignment,end=" ")
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)