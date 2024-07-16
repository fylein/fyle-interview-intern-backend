from flask import Blueprint, jsonify
from core import db
from core.apis.responses import APIResponse
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from .. import decorators
from core.apis.decorators import accept_payload, authenticate_principal

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_assignments(p):
    try:
        # Example: Fetch assignments based on principal ID
        assignments = Assignment.query.filter(
            (Assignment.state == AssignmentStateEnum.GRADED) | (Assignment.state == AssignmentStateEnum.SUBMITTED)
        ).all()

        assignment_schema = AssignmentSchema(many=True)
        return APIResponse.respond(data=assignment_schema.dump(assignments))

    except FyleError as e:
        # Handle specific error for principal ID not found
        return APIResponse.respond_error(message=str(e), status_code=404)

    except Exception as e:
        # Handle unexpected errors
        return APIResponse.respond_error(message='Internal Server Error', status_code=500)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@accept_payload
@authenticate_principal
def grade_assignment(p, incoming_payload):
    try:
        # Load and validate incoming payload
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

        # Retrieve assignment from database
        assignment = Assignment.query.get(grade_assignment_payload.id)
        if not assignment:
            raise FyleError("Assignment not found", status_code=404)

        # Check assignment state
        if assignment.state == AssignmentStateEnum.DRAFT:
            raise FyleError("Assignment in DRAFT state cannot be graded", status_code=400)

        # Mark assignment as graded
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )

        # Commit changes to database
        db.session.commit()

        # Serialize graded assignment to JSON
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

        # Return successful response
        return APIResponse.respond(data=graded_assignment_dump)

    except FyleError as e:
        # Handle specific FyleError exceptions
        return APIResponse.respond_error(message=str(e), status_code=e.status_code)

    except Exception as e:
        # Handle unexpected errors
        return APIResponse.respond_error(message='Internal Server Error', status_code=500)