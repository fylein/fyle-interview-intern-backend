""" 
workflow:
> we 're going to create a Blueprint so that all the views associated to the principal is grouped and managed from here.
> then we 're going to register the required views for /assignments, /teachers, /assignments/grade
"""

from flask import Blueprint
from core.apis import decorators
from core.models.assignments import Assignment, Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema
from core.apis.responses import APIResponse
from core import db

# created a blueprint to manage all the resources from principal.py only.
principal_resources = Blueprint('principal_resources', __name__)


# GET /principal/assignments
@principal_resources.route("/assignments", methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of graded or submitted assignments"""
    submitted_or_graded_assignment = Assignment.get_submitted_or_graded_assignments(
    )  # this is a python obj that we want to store persistently inside a db.
    principal_assignments_dump = AssignmentSchema().dump(
        submitted_or_graded_assignment, many=True)  # but before that we need to serialize it so that it could be sent over the wire.
    return APIResponse.respond(data=principal_assignments_dump)

# GET /principal/teachers
@principal_resources.route("/teachers", methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teachers(p):
    """ Returns a list of  the Teachers. """
    teachers = Teacher.list_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


# POST /principal/assignments/grade
@principal_resources.route("/assignments/grade", methods=['POST'] , strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignments(p, incoming_payload):
    assignment_to_grade_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.regrade(
        _id=assignment_to_grade_payload.id,
        grade=assignment_to_grade_payload.grade
        )
    
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
