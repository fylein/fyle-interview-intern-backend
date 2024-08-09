from flask import Blueprint
from marshmallow import ValidationError
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

    # Load and validate the incoming payload using the Assignment schema
    try:
        assignment = AssignmentSchema().load(incoming_payload)
    except ValidationError as e:
        return APIResponse.respond(
            error='BadRequest',
            message='Invalid assignment data',
            status_code=400
        )
    
    # Set the student_id from the authenticated principal
    assignment.student_id = p.student_id

    # Upsert the assignment in the database
    upserted_assignment = Assignment.upsert(assignment)

    # Commit the transaction to the database
    db.session.commit()

    # Serialize the upserted assignment
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)

    # Return the response
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
        auth_principal=p
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
