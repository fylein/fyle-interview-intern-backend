from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.models.teachers import Teacher
from .schema import TeacherSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint(
    'principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_and_graded_assignments(p):
    principal_assignments = Assignment.filter(
        Assignment.state.in_(
            [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()

    assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    # Grade or re-grade an assignment
    grade_or_regrade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_or_regrade_assignment_payload.id)

    if assignment.state == 'DRAFT':
        return APIResponse.respond_error('FyleError', 'Cannot grade an assignment in DRAFT state', 400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_or_regrade_assignment_payload.id,
        grade=grade_or_regrade_assignment_payload.grade,
        auth_principal=p
    )

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
