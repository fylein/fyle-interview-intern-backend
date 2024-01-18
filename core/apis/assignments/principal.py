from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.apis.assignments.schema import AssignmentSchema
from core.models.teachers import Teacher

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_principal_assignments(p):
    assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    assignment_data = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignment_data)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    if not decorators.authenticate_principal(p):
        return APIResponse.respond(status_code = 403)
    assignment_id = incoming_payload.get('id')
    grade = incoming_payload.get('grade')
    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        return APIResponse.respond(data = None), 404

    if assignment.state == AssignmentStateEnum.DRAFT.value:
        return APIResponse.respond(data = None), 400
    assignment = Assignment.mark_grade(assignment_id, grade, p)
    db.session.commit()
    assignment_data = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_data)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_principal_teachers(p):
    teachers = Teacher.query.all()
    teacher_data = []
    for i in teachers:
        teacher_data.append({
            'id': i.id,
            'user_id': i.user_id,
            'created_at': str(i.created_at),
            'updated_at': str(i.updated_at)
        })
    return APIResponse.respond(data=teacher_data)
