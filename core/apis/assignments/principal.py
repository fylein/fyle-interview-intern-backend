from flask import Blueprint
from core.apis import decorators
from core import db
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, Teacher
from core.apis.teachers.schema import TeacherSchema
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)
# feature: Implementing APIs
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_assignments(p):
    """Returns a list of submitted and graded assignments"""
    assignments = Assignment.list_all_graded_submitted_assignments()
    assignments_data = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_data)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)