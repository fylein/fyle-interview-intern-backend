from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema

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
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

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

    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        principal=p
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)


@student_assignments_resources.route('/assignments/<int:assignment_id>', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_assignment(p, assignment_id):
    assignment = Assignment.get_assignment_by_id(assignment_id, p.student_id)
    if assignment:
        assignment_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=assignment_dump)
    else:
        data = {"message": "No assignment was found"}
        return APIResponse.respond(data=data)


@student_assignments_resources.route('/assignments/drafts', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_draft_assignments(p):
    """List draft assignments"""
    draft_assignments = Assignment.get_draft_assignments_by_student(p.student_id)
    draft_assignments_dump = AssignmentSchema().dump(draft_assignments, many=True)
    return APIResponse.respond(data=draft_assignments_dump)


@student_assignments_resources.route('/assignments/submitted', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_assignments(p):
    """List submitted assignments"""
    submitted_assignments = Assignment.get_submitted_assignments_by_student(p.student_id)
    submitted_assignments_dump = AssignmentSchema().dump(submitted_assignments, many=True)
    return APIResponse.respond(data=submitted_assignments_dump)
