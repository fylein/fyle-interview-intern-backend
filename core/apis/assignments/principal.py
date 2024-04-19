from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_principal_assignments(principal):
    """List all submitted and graded assignments."""
    principal_assignments = Assignment.get_submitted_and_graded_assignments()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teachers(principal):
    """List all teachers."""
    teachers = Teacher.query.all()
    teachers_dump = [{'id': teacher.id, 'created_at': teacher.created_at, 'updated_at': teacher.updated_at,
                      'user_id': teacher.user_id} for teacher in teachers]
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p,incoming_payload):
    """Grade or re-grade an assignment."""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)
