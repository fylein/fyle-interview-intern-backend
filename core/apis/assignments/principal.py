from flask import Blueprint, request, jsonify
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from core import db
from core.apis.responses import APIResponse
from core.apis import decorators

# Create blueprint for principal routes
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# =============================
# API: GET /principal/assignments
# Description: Fetch all assignments that are either submitted or graded.
# =============================
@principal_assignments_resources.route('/assignments', methods=['GET'])
def get_all_assignments():
    try:
        assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
        if not assignments:
            return jsonify({"message": "No assignments found"}), 404
        response = [assignment.to_dict() for assignment in assignments]
        return jsonify({"data": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# API: GET /principal/teachers
# Description: Fetch all the teachers.
# =============================
@principal_assignments_resources.route('/teachers', methods=['GET'])
def get_all_teachers():
    try:
        teachers = Teacher.query.all()
        if not teachers:
            return jsonify({"message": "No teachers found"}), 404
        response = [teacher.to_dict() for teacher in teachers]
        return jsonify({"data": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@principal_assignments_resources.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    try:
        
        data = request.get_json()
        assignment_id = data.get('id')
        new_grade = data.get('grade')

        if not assignment_id or not new_grade:
            return jsonify({"error": "Missing assignment ID or grade"}), 400

        assignment = Assignment.query.filter_by(id=assignment_id).first()
        print(f"Assignment ID: {assignment_id}, State: {assignment.state}")  # Add this line

        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

         # Check if the assignment is in draft state
        if assignment.state == AssignmentStateEnum.DRAFT:
            return jsonify({"error": "Assignment is in draft state and cannot be graded"}), 400

        assignment.grade = new_grade
        assignment.state = 'GRADED'
        db.session.commit()
        return jsonify({"data": assignment.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
