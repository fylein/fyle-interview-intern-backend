from flask import Blueprint,jsonify,request
from core.libs.assertions import base_assert
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    authorization_header = request.headers.get('Authorization')
    teachers_assignments = Assignment.get_assignments_by_teacher(teacher_id=authorization_header)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    headers=request.headers.get('Authorization')
    assignment=Assignment.get_by_id(grade_assignment_payload.id)
    if assignment != None:
        teacher_id=assignment.teacher_id
        if(headers==teacher_id):
            graded_assignment = Assignment.mark_grade(
                _id=grade_assignment_payload.id,
                grade=grade_assignment_payload.grade,
                auth_principal=p
            )   
            db.session.commit()
            graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
            return APIResponse.respond(data=graded_assignment_dump)
        return base_assert(400,"Error")
    return base_assert(404,"No Assignment Found")