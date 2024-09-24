# teachers/principal.py
from flask import Blueprint, request, jsonify
from core.models import Assignment, Teacher, db  # Assuming Assignment and Teacher models exist in your project
from sqlalchemy import and_
from .schema import PrincipalAssignmentSchema, TeacherSchema

# Define Blueprint for principal-related actions
principal_bp = Blueprint('principal', __name__)

# GET /principal/assignments - List all submitted and graded assignments
@principal_bp.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    assignments = Assignment.query.filter(
        Assignment.state.in_(['SUBMITTED', 'GRADED'])
    ).all()

    # Serialize the assignments using PrincipalAssignmentSchema
    assignment_schema = PrincipalAssignmentSchema(many=True)
    data = assignment_schema.dump(assignments)

    return jsonify({'data': data})

# GET /principal/teachers - List all teachers
@principal_bp.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    teachers = Teacher.query.all()

    # Serialize the teachers using TeacherSchema
    teacher_schema = TeacherSchema(many=True)
    data = teacher_schema.dump(teachers)

    return jsonify({'data': data})

# POST /principal/assignments/grade - Grade or re-grade an assignment
@principal_bp.route('/principal/assignments/grade', methods=['POST'])
def regrade_assignment():
    data = request.get_json()
    assignment_id = data.get('id')
    new_grade = data.get('grade')

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    # Update the grade of the assignment
    assignment.grade = new_grade
    db.session.commit()

    # Serialize the updated assignment
    assignment_schema = PrincipalAssignmentSchema()
    response = assignment_schema.dump(assignment)

    return jsonify({'data': response})
