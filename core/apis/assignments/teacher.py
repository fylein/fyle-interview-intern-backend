from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment


from .schema import AssignmentSchema,AssignmentSubmitSchema,AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)



@teacher_assignments_resources.route('assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_teacher_assignments(p):
    """Returns list of assignments submitted to this teacher"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    print(incoming_payload)
    """Grade an assignment"""
    grade_payload = AssignmentGradeSchema().load(incoming_payload)
    grading_assignment = Assignment.assign_grade(
        _id=grade_payload.id,
        grade=grade_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment = Assignment.get_by_id(grade_payload.id)
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)