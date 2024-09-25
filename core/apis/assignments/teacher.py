from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    print("teacher_id", p.teacher_id)
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""

    print('incoming_payload["grade"]', incoming_payload["grade"])
    assignment = Assignment.get_by_id(incoming_payload["id"])
    assignment_dump = AssignmentSchema().dump(assignment)

    if not assignment:
        print("1")
        return jsonify({"error": "FyleError"}), 404

    if incoming_payload["grade"] not in GradeEnum:
        print("4")
        return jsonify({"error": "ValidationError"}), 400

    if assignment_dump["state"] != AssignmentStateEnum.SUBMITTED:
        print("2")
        return jsonify({"error": "FyleError"}), 400

    if assignment_dump["teacher_id"] != p.teacher_id:
        print("3")
        return jsonify({"error": "FyleError"}), 400



    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
