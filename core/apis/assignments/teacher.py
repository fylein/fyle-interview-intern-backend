from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema



teacher_resourses  = Blueprint("teacher_resourses", __name__)

@teacher_resourses.route("/assignments", methods = ["GET"])
@decorators.auth_principal
def list_all_assignment_for_teacher(p):
    """Returns all the assignment submitted to the teacher"""
    all_submitted_assignments = Assignment.get_assignments_submitted_to_teacher(teacher_id=p.teacher_id)
    all_assignments_dump = AssignmentSchema().dump(all_submitted_assignments, many = True)
    return APIResponse.respond(data=all_assignments_dump)


@teacher_resourses.route("/assignments/grade", methods=["POST"])
@decorators.accept_payload
@decorators.auth_principal
def grade_assignmnet(p, payload):
    """Grade assignmnent of student"""

    print(f"\npayload : {payload['id']}, {payload['grade']}\n")
    assignment = Assignment.grade_assignment(payload["id"], payload["grade"], p)

    assignment_dump = AssignmentSchema().dump(assignment)
    print(f"\n assignment dump {assignment_dump}\n")

    return APIResponse.respond(assignment_dump)

    

