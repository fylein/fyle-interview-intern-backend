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
    '''
    GET request to list all assignments which are:
    1. submitted
    2. graded
    '''
    assignments = AssignmentSchema().dump(Assignment.get_assignments_by_principal(), many=True)
    return APIResponse.respond(data=assignments)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal      
def grade_assignments(p, incoming_payload):
    '''POST request to update grade of an assignment.'''
    payload_data = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment_data = Assignment.mark_grade(
        _id=payload_data.id,
        grade=payload_data.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment = AssignmentSchema().dump(graded_assignment_data)
    return APIResponse.respond(data=graded_assignment)