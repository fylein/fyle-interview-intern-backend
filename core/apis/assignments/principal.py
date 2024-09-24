from flask import Blueprint, jsonify

principal_assignments_resources = Blueprint('principal_assignments', __name__)

@principal_assignments_resources.route('/principal/assignments', methods=['GET'])
def get_all_assignments():
    # Logic to retrieve all submitted and graded assignments
    assignments = Assignment.query.all()  # Replace with actual DB query
    return jsonify({"data": [assignment.serialize() for assignment in assignments]})

@principal_assignments_resources.route('/principal/teachers', methods=['GET'])
def get_all_teachers():
    # Logic to retrieve all teachers
    teachers = Teacher.query.all()  # Replace with actual DB query
    return jsonify({"data": [teacher.serialize() for teacher in teachers]})
@principal_assignments_resources.route('/principal/assignments/grade', methods=['POST'])
def regrade_assignment():
    data = request.get_json()
    assignment_id = data.get('id')
    new_grade = data.get('grade')

    assignment = Assignment.query.get(assignment_id)
    if assignment:
        assignment.grade = new_grade
        db.session.commit()
        return jsonify({"data": assignment.serialize()})
    else:
        return jsonify({"error": "Assignment not found"}), 404

