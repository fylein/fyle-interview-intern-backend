from flask import Blueprint, jsonify
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
    
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    if assignment.content is not None:
        upserted_assignment = Assignment.upsert(assignment)
        db.session.commit()
        upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
        return APIResponse.respond(data=upserted_assignment_dump)
    else:
        return jsonify(error='Content is null! Content cannot be empty'), 400


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""

    try:
        # Attempt to load the payload based on the schema
        submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

        # Fetch the assignment based on the provided ID
        assignment = Assignment.get_by_id(submit_assignment_payload.id)

        # Check if the assignment is in the "DRAFT" state
        if assignment.state != 'DRAFT':
            # Return an error response if the assignment is not in the draft state
            return APIResponse.respond(
                data={'error': 'FyleError', 'message': 'only a draft assignment can be submitted'},
                status=400  # Change this to 'status' instead of 'status_code'
            )

        # Submit the assignment if it's in the "DRAFT" state
        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth_principal=p
        )

        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
        return APIResponse.respond(data=submitted_assignment_dump)

    except ValidationError as e:
        # Catch schema validation errors and return them
        return APIResponse.respond(
            data={'error': 'ValidationError', 'messages': e.messages},
            status=400
        )

    except KeyError as e:
        # Catch unexpected key error and return a meaningful error message
        return APIResponse.respond(
            data={'error': 'KeyError', 'message': f'Unexpected key: {str(e)}'},
            status=400
        )

