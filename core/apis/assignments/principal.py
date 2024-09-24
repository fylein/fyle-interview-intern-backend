from flask import Blueprint,jsonify,request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from .schema import AssignmentSchema,AssignmentGradeSchema


principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


#principal route setup
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of all submitted and graded assignments"""
    assignments = Assignment.list_all_graded_submitted_assignments()
    assignments_data = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_data)

@principal_assignments_resources.route('/teachers', methods=['GET'])
def get_all_teachers():
    try:
        teachers = Teacher.query.all()
        if not teachers:
            return jsonify({"message": "No teachers found"}), 400
        response = [teacher.to_dict() for teacher in teachers]
        return jsonify({"data": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@principal_assignments_resources.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    data = request.get_json()
    assignment_id = data.get('id')
    new_grade = data.get('grade')
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 400
    if assignment.state == AssignmentStateEnum.DRAFT:
        return jsonify({"error": "Assignment is in draft state and cannot be graded"}), 400

    assignment.grade = new_grade
    assignment.state = 'GRADED'
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)