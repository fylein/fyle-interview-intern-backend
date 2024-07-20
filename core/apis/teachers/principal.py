from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.assignments import Assignment
from .schema import TeacherSchema, AssignmentSchema, AssignmentGradeSchema

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all teachers"""
    try:
        teachers = Teacher.query.all()
        teachers_dump = TeacherSchema(many=True).dump(teachers)
        return APIResponse.respond(data=teachers_dump)
    except Exception as e:
        # Log the exception for debugging purposes
        current_app.logger.error(f"Error listing teachers: {e}")
        return APIResponse.respond_error(message='Internal server error', status_code=500)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """List all assignments"""
    try:
        assignments = Assignment.query.all()
        assignments_dump = AssignmentSchema(many=True).dump(assignments)
        return APIResponse.respond(data=assignments_dump)
    except Exception as e:
        # Log the exception for debugging purposes
        current_app.logger.error(f"Error listing assignments: {e}")
        return APIResponse.respond_error(message='Internal server error', status_code=500)

@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    try:
        assignment_grade_payload = AssignmentGradeSchema().load(incoming_payload)
        assignment = Assignment.query.filter_by(id=assignment_grade_payload.id).first()
        if not assignment:
            return APIResponse.respond_error(message='Assignment not found', status_code=404)

        assignment.grade = assignment_grade_payload.grade
        assignment.state = 'GRADED'  # Assuming state should be updated to 'GRADED'
        db.session.commit()

        assignment_dump = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=assignment_dump)
    except Exception as e:
        # Log the exception for debugging purposes
        current_app.logger.error(f"Error grading assignment: {e}")
        db.session.rollback()  # Rollback the session in case of error
        return APIResponse.respond_error(message='Internal server error', status_code=500)
