from flask import Blueprint
from core import db
from core.apis import decorators,responses
from .schema import AssignmentGradeSchema, AssignmentSchema, TeacherSchema
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher


principal_assig_app = Blueprint("principal_assig_app",__name__)

@principal_assig_app.route("/assignments",methods=["GET"],strict_slashes=False)
@decorators.authenticate_principal
def get_all_assigments(r):
    """Return All Assignments that are Graded and Submited"""
    all_assig = Assignment.filter(Assignment.grade == AssignmentStateEnum.GRADED and Assignment.state == AssignmentStateEnum.SUBMITTED)
    all_assig_dmp = AssignmentSchema().dump(all_assig,many=True)
    return responses.APIResponse.respond(data=all_assig_dmp)


@principal_assig_app.route("/assignments/grade",methods=["POST"],strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def add_grade_to_assig(r,payload):
    """Grade the Assignment authorized by principal"""
    data  = AssignmentGradeSchema().load(payload)
    updated_assign = Assignment.mark_grade(
        _id = data.id,
        grade=data.grade,
        auth_principal=r
    )
    db.session.commit()
    updated_assign_dmp = AssignmentSchema().dump(updated_assign)
    return responses.APIResponse.respond(updated_assign_dmp)

@principal_assig_app.route("/teachers",methods=["GET"],strict_slashes=False)
@decorators.authenticate_principal
def get_all_teachers(r):
    all_teachers = Teacher.query.all()
    all_teacher_dmp = TeacherSchema().dump(all_teachers,many=True)
    return responses.APIResponse.respond(all_teacher_dmp)








