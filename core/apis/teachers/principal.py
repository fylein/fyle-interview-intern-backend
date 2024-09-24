from flask import Blueprint, jsonify
from core.models import Assignment, User  # Import the necessary models
from core.libs.helpers import ensure_principal  # Ensure only principals can access

# Create a blueprint for principal-related APIs
principal_resources = Blueprint('principal_resources', __name__)

# Route to get all submitted and graded assignments
@principal_resources.route('/principal/assignments', methods=['GET'])
@ensure_principal
def get_principal_assignments():
    # Query the assignments with 'SUBMITTED' or 'GRADED' states
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    
    # Convert the assignments into a JSON-serializable format
    assignments_data = [assignment.to_dict() for assignment in assignments]
    
    # Return the JSON response
    return jsonify({'data': assignments_data})

# Route to get all teachers
@principal_resources.route('/principal/teachers', methods=['GET'])
@ensure_principal
def get_principal_teachers():
    # Query all users who have the role of 'TEACHER'
    teachers = User.query.filter_by(role='TEACHER').all()
    
    # Convert the teachers into a JSON-serializable format
    teachers_data = [teacher.to_dict() for teacher in teachers]
    
    # Return the JSON response
    return jsonify({'data': teachers_data})
