from flask import Blueprint, jsonify

from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from ...models.teachers import Teacher

principal_assigment_resources = Blueprint('principal_assigment_resources', __name__)


@principal_assigment_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(_p):
    """Returns list of assignment"""
    principal_teachers = Assignment.get_all_assignment()
    principal_teachers_dump = AssignmentSchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=principal_teachers_dump)


@principal_assigment_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(incoming_payload["id"])
    assignment_dump = AssignmentSchema().dump(assignment)

    if not assignment:
        return jsonify({"error": "Assignment not found."}), 404

    if incoming_payload["grade"] not in GradeEnum:
        return jsonify({"error": "ValidationError"}), 400

    if assignment_dump["state"] != AssignmentStateEnum.DRAFT:
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
    else:
        return jsonify({"error": "Assignment is still in DRAFT status and cannot be graded."}), 400

