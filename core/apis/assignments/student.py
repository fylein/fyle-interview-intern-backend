from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from marshmallow import ValidationError
from core.models.assignments import Assignment, AssignmentStateEnum

from core.apis.assignments.schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    try:
        assignment = AssignmentSchema().load(incoming_payload)
    except ValidationError as err:
        # print(f"Validation error: {err.messages}")
        return jsonify({"error": "ValidationError", "message": str(err.messages)}), 400
    
    assignment.student_id = p.student_id
    assignment.principal_id = 1

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    assignment = Assignment.query.get(submit_assignment_payload.id)

    
    if assignment is None:
        raise BadRequest(description='Assignment not found')

    
    if assignment.state != AssignmentStateEnum.DRAFT:
        raise BadRequest(description='Only a draft assignment can be submitted')


    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    # assignment.state = AssignmentStateEnum.SUBMITTED
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
