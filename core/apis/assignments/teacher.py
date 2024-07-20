from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def create_assignment(p, incoming_payload):
    """Create a new assignment"""
    new_assignment_payload = AssignmentSchema().load(incoming_payload)

    new_assignment = Assignment(
        content=new_assignment_payload.content,
        teacher_id=p.id
    )
    db.session.add(new_assignment)
    db.session.commit()
    new_assignment_dump = AssignmentSchema().dump(new_assignment)
    return APIResponse.respond(data=new_assignment_dump)
