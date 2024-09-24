from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
import logging

from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the blueprint for principal-specific APIs
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

### 1. GET /principal/assignments
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

### 2. GET /principal/teachers
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)

### 3. POST /principal/assignments/grade
@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    assignment = Assignment.query.get(grade_assignment_payload.id)
    
    if not assignment:
        return APIResponse.respond_with_error('Assignment not found', 404)

    # Ensure the assignment is in a submitted state before grading
    if assignment.state != 'SUBMITTED':
        return APIResponse.respond_with_error('Assignment cannot be graded in its current state', 400)
    
    # Update the grade and state of the assignment
    assignment.grade = grade_assignment_payload.grade
    assignment.state = 'GRADED'
    
    # Commit changes to the database
    try:
        db.session.commit()
        logger.info(f'Assignment {assignment.id} graded with {assignment.grade}')
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error grading assignment {assignment.id}: {e}')
        return APIResponse.respond_with_error('Failed to grade assignment', 500)
    
    assignment_dump = AssignmentSchema().dump(assignment)
    
    return APIResponse.respond(data=assignment_dump, message='Assignment graded successfully.')