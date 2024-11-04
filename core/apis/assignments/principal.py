from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    assignments_list = Assignment.get_assignments_by_principal()
    serialized_assignments = AssignmentSchema().dump(assignments_list, many=True)
    return APIResponse.respond(data=serialized_assignments)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal      
def grade_assignments(p, incoming_payload):
    validated_payload = AssignmentGradeSchema().load(incoming_payload)

    updated_assignment = Assignment.mark_grade(
        _id=validated_payload.id,
        grade=validated_payload.grade,
        auth_principal=p
    )
    db.session.commit()

    result = AssignmentSchema().dump(updated_assignment)
    return APIResponse.respond(data=result)