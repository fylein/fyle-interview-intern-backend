
from flask import Blueprint
from core.apis import decorators
from core import db
from core.apis.assignments.schema import AssignmentGradeSchema, AssignmentSchema
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of all assignments"""
    students_assignments = Assignment.get_all_assignments()
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)
    
@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment only"""
    id_payload = incoming_payload['id']
    assignment = Assignment.get_by_id(id_payload)
    
    if assignment.state == AssignmentStateEnum.DRAFT:
        return (APIResponse.respond(data="Cannot Grade a Draft Assignment"), 400)
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
