from flask import Blueprint
from core.apis import decorators
from core import db
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

# Define blueprint for principal assignment resources
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# Feature: Implementing APIs for the principal
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
    """Returns a list of submitted and graded assignments"""
    # Retrieve all graded and submitted assignments
    assignments = Assignment.list_all_graded_submitted_assignments()
    
    # Serialize assignment data
    assignments_data = AssignmentSchema().dump(assignments, many=True)
    
    # Return the list of assignments as a response
    return APIResponse.respond(data=assignments_data)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    # Load and validate the payload
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    # Mark the assignment as graded
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    
    # Commit the grade changes to the database
    db.session.commit()
    
    # Serialize the graded assignment data
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    # Return the graded assignment details as a response
    return APIResponse.respond(data=graded_assignment_dump)
    