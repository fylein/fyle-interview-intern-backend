from flask import Blueprint
from core import db
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.apis.responses import APIResponse
from .schema import AssignmentSchema,AssignmentGradeSchema
from core.apis import decorators

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# API for listing assignments

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principle_assignments = Assignment.get_submitted_and_graded_assignments()
    principle_assignments_dump = AssignmentSchema().dump(principle_assignments, many=True)
    return APIResponse.respond(data=principle_assignments_dump)

# API for listing teachers

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_all_teachers()
    teachers_data = []
    for teacher in teachers:
        teachers_data.append({
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at.isoformat(),
            'updated_at': teacher.updated_at.isoformat()
        })

    return APIResponse.respond(data=teachers_data)


# API for re-grading an assignment

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.regrade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


