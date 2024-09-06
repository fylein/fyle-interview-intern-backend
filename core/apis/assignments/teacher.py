from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs import assertions
from ...libs.exceptions import FyleError

from .schema import AssignmentSchema, AssignmentGradeSchema

# Define blueprint for teacher assignment resources
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    # Return assignments based on teacher_id
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    # Check if the payload is missing
    if not incoming_payload:
        assertions.assert_valid(None, "Payload is missing")
    
    # Load grade assignment payload
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    
    # Handle assignment not found
    if assignment is None:
        raise FyleError(404, 'Assignment not found')
    
    # Validate the teacher's ownership of the assignment
    if p.teacher_id != assignment.teacher_id:
        raise FyleError(400, 'Assignment submitted to another teacher')
    
    # Mark and grade the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return the graded assignment details
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
