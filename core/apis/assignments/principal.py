from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods = ['GET'], strict_slashes = False)

@decorators.authenticate_principal
def get_all_assignments(p):
    """Returns graded assignments and submitted assignments"""
    principal_assignments_get = Assignment.filter(Assignment.state != AssignmentStateEnum.DRAFT).all()
    principal_assignments_get_dump = AssignmentSchema().dump(principal_assignments_get, many=True)
    return APIResponse.respond(data = principal_assignments_get_dump)


@principal_assignments_resources.route('/assignments/grade', methods = ['POST'], strict_slashes = False)

@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p,incoming_payload):
    """Grade an Assignment"""
    assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    marking_grade = Assignment.mark_grade_by_principal(_id= assignment_payload.id,grade=assignment_payload.grade, auth_principal=p)
    db.session.commit()
    marking_grade_dump = AssignmentSchema().dump(marking_grade)
    return APIResponse.respond(data=marking_grade_dump)
    
    

    