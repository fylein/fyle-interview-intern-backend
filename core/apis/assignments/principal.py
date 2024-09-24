from flask import Blueprint, request, jsonify
from core.models import Assignment, Teacher, db  # Assuming you have models for Assignment, Teacher, and access to the database
from sqlalchemy import and_

principal_bp = Blueprint('principal', __name__)

# GET /principal/assignments - List all submitted and graded assignments
@principal_bp.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    assignments = Assignment.query.filter(
        Assignment.state.in_(['SUBMITTED', 'GRADED'])  # Filter only submitted and graded assignments
    ).all()

    data = [{
        'content': assignment.content,
        'created_at': assignment.created_at,
        'grade': assignment.grade,
        'id': assignment.id,
        'state': assignment.state,
        'student_id': assignment.student_id,
        'teacher_id': assignment.teacher_id,
        'updated_at': assignment.updated_at
    } for assignment in assignments]

    return jsonify({'data': data})

# GET /principal/teachers - List all teachers
@principal_bp.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    teachers = Teacher.query.all()

    data = [{
        'id': teacher.id,
        'user_id': teacher.user_id,
        'created_at': teacher.created_at,
        'updated_at': teacher.updated_at
    } for teacher in teachers]

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

    # Update grade
    assignment.grade = new_grade
    db.session.commit()

    response = {
        'content': assignment.content,
        'created_at': assignment.created_at,
        'grade': assignment.grade,
        'id': assignment.id,
        'state': 'GRADED',
        'student_id': assignment.student_id,
        'teacher_id': assignment.teacher_id,
        'updated_at': assignment.updated_at
    }

    return jsonify({'data': response})
