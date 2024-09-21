from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


# API Endpoint : /principal/assignments
@principal_assignments_resources.route(
    "/assignments", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def get_all_submitted_and_graded_assignments(p):
    # List all submitted and graded assignment
    all_submitted_and_graded_assignments = (
        Assignment.list_all_submitted_and_graded_assignments()
    )

    all_submitted_and_graded_assignments_dump = AssignmentSchema().dump(
        all_submitted_and_graded_assignments, many=True
    )
    return APIResponse.respond(data=all_submitted_and_graded_assignments_dump)


# API Endpoint : /principal/assignments/grade
@principal_assignments_resources.route(
    "/assignments/grade", methods=["POST"], strict_slashes=False
)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    # Grade or re-grade an assignment
    grade_or_regrade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_or_regraded_assignment = Assignment.mark_grade(
        _id=grade_or_regrade_assignment_payload.id,
        grade=grade_or_regrade_assignment_payload.grade,
        auth_principal=p,
    )
    db.session.commit()
    graded_or_regraded_assignment_dump = AssignmentSchema().dump(
        graded_or_regraded_assignment
    )
    return APIResponse.respond(data=graded_or_regraded_assignment_dump)
