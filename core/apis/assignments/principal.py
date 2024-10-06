from flask import Blueprint, abort
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema,TeacherSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principals_assignments = Assignment.get_assignments_by_principal(p)
    principals_assignments_dump = AssignmentSchema().dump(principals_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = db.session.get(Assignment, grade_assignment_payload.id)
    if assignment is None:
        return APIResponse.respond({'error':'FyleError', 'message':'assignment does not exist'},status=404)
    if assignment.state == AssignmentStateEnum.DRAFT.value:
        return APIResponse.respond({'error':'FyleError', 'message':'assignment is in draft state'},status=400)
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teachers(p):
    """Get list of teachers"""
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)

