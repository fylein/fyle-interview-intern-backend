from flask import Blueprint, request, jsonify, current_app as app
from core.models import db, Assignment, Teacher
from core.libs.exceptions import FyleError

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'])
def get_assignments():
    try:
        assignments = Assignment.query.all()
        return jsonify({'data': [assignment.to_dict() for assignment in assignments]})
    except Exception as e:
        app.logger.error(f"Error retrieving assignments: {e}")
        return jsonify({'error': 'InternalServerError', 'message': 'Error retrieving assignments'}), 500

@principal_resources.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        teachers = Teacher.query.all()
        return jsonify({'data': [teacher.to_dict() for teacher in teachers]})
    except Exception as e:
        app.logger.error(f"Error retrieving teachers: {e}")
        return jsonify({'error': 'InternalServerError', 'message': 'Error retrieving teachers'}), 500

@principal_resources.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    data = request.get_json()
    assignment_id = data.get('id')
    grade = data.get('grade')

    if not assignment_id or not grade:
        return jsonify({'error': 'BadRequest', 'message': 'Missing assignment ID or grade'}), 400

    valid_grades = {'A', 'B', 'C', 'D'}
    if grade not in valid_grades:
        return jsonify({'error': 'BadRequest', 'message': 'Invalid grade'}), 400

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'error': 'NotFound', 'message': 'Assignment not found'}), 404

    assignment.grade = grade
    assignment.state = 'GRADED'
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating assignment grade: {e}")
        return jsonify({'error': 'InternalServerError', 'message': 'Error updating assignment grade'}), 500

    return jsonify({'data': assignment.to_dict()})
