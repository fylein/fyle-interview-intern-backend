from flask import Blueprint, jsonify, request
from core.models import Assignment, User  # Import the necessary models
from core.libs.helpers import ensure_principal  # Ensure only principals can access
from core.libs.exceptions import FyleError

# Create a blueprint for principal-related APIs
# The Blueprint name has been changed to match what is being imported in core/server.py
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# Route to get all submitted and graded assignments
@principal_assignments_resources.route('/principal/assignments', methods=['GET'])
@ensure_principal
def get_principal_assignments():
    # Query the assignments with 'SUBMITTED' or 'GRADED' states
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    
    # Convert the assignments into a JSON-serializable format
    assignments_data = [assignment.to_dict() for assignment in assignments]
    
    # Return the JSON response
    return jsonify({'data': assignments_data})

# Route to get all teachers
@principal_assignments_resources.route('/principal/teachers', methods=['GET'])
@ensure_principal
def get_principal_teachers():
    # Query all users who have the role of 'TEACHER'
    teachers = User.query.filter_by(role='TEACHER').all()
    
    # Convert the teachers into a JSON-serializable format
    teachers_data = [teacher.to_dict() for teacher in teachers]
    
    # Return the JSON response
    return jsonify({'data': teachers_data})

# Route to re-grade an assignment
@principal_assignments_resources.route('/principal/assignments/grade', methods=['POST'])
@ensure_principal
def regrade_assignment():
    payload = request.json
    assignment_id = payload.get('id')
    new_grade = payload.get('grade')

    # Fetch the assignment
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        raise FyleError("Assignment not found", 404)

    # Update the assignment grade
    assignment.grade = new_grade
    assignment.state = 'GRADED'

    # Commit the changes to the database
    assignment.save()

    # Return the updated assignment as a response
    return jsonify({'data': assignment.to_dict()})
