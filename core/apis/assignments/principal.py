from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


@principal_assignments_resources.route("/assignments", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments_for_principal(p):
    """List all submitted and graded assignments for the principal."""
    assignments = Assignment.get_assignments_for_principal(p.principal_id)
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route("/teachers", methods=["GET"], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all teachers for the principal."""
    teachers = Assignment.get_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route("/assignments/grade", methods=["POST"], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment_for_principal(p, incoming_payload):
    """Grade or re-grade an assignment for the principal."""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id, grade=grade_assignment_payload.grade, auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
