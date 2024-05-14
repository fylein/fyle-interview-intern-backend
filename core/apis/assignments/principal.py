from core.models.assignments import Assignment,AssignmentStateEnum
from flask import jsonify, Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs.assertions import assert_found,assert_valid

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_assignments(p):
    assignments = Assignment.filter(Assignment.state != AssignmentStateEnum.DRAFT).all()
    data = AssignmentSchema().dump(assignments,many=True)
    return APIResponse.respond(data=data)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p,incoming_payload):
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
        assignment_id = grade_assignment_payload.id
        grade = grade_assignment_payload.grade

        assignment = Assignment.get_by_id(assignment_id)
        assert_found(assignment)
        assert_valid(assignment.state != AssignmentStateEnum.DRAFT, 'Cannot grade a draft assignment')
        
        assignment.state = AssignmentStateEnum.GRADED
        assignment.grade = grade
        db.session.commit()

        data = AssignmentSchema().dump(assignment)
        return APIResponse.respond(data=data)