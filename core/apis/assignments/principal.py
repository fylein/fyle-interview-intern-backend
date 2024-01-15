from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentSubmitSchema , TeacherSchema , AssignmentGradeSchema
from core.libs.exceptions import FyleError
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments graded or submitted"""
    principal_assignments = Assignment.get_submitted_graded()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_regrade_assignment(p,incoming_payload):
    """Graded/regraded assignments"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    if incoming_payload['grade'] not in {'A', 'B', 'C', 'D'}:
        print(incoming_payload["grade"])
        raise FyleError(400, 'invalid grade')
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
    
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of Teachers"""
    principal_teachers=Teacher.get_all()
    principal_teachers_dump=TeacherSchema().dump(principal_teachers,many=True)
    return APIResponse.respond(data=principal_teachers_dump)

    

# @student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def upsert_assignment(p, incoming_payload):
#     """Create or Edit an assignment"""
#     assignment = AssignmentSchema().load(incoming_payload)
#     assignment.student_id = p.student_id

#     upserted_assignment = Assignment.upsert(assignment)
#     db.session.commit()
#     upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
#     return APIResponse.respond(data=upserted_assignment_dump)


# @student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def submit_assignment(p, incoming_payload):
#     """Submit an assignment"""
#     submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

#     submitted_assignment = Assignment.submit(
#         _id=submit_assignment_payload.id,
#         teacher_id=submit_assignment_payload.teacher_id,
#         auth_principal=p
#     )
#     db.session.commit()
#     submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
#     return APIResponse.respond(data=submitted_assignment_dump)
