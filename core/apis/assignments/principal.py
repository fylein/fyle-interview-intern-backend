from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema


from .schema import AssignmentSchema, AssignmentSubmitSchema

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)

#############


def get_all_teachers():
    # Create a SQLAlchemy session
    with db.session() as session:
        # Query the database for all teachers, including the user_id column
        teachers = session.query(Teacher).all()

        # Convert each teacher object to a dictionary
        teachers_data = [
            {
                "created_at": teacher.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                "id": teacher.id,
                "updated_at": teacher.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                "user_id": teacher.user_id,
            }
            for teacher in teachers
        ]

        # Return the list of teacher dictionaries
        return teachers_data


#######################


@principal_assignments_resources.route(
    "/assignments", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    all_graded_submitted_assignments = Assignment.get_assignments_submitted_or_graded()
    all_graded_submitted_assignments_dump = AssignmentSchema().dump(
        all_graded_submitted_assignments, many=True
    )
    return APIResponse.respond(data=all_graded_submitted_assignments_dump)


@principal_assignments_resources.route(
    "/teachers", methods=["GET"], strict_slashes=False
)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    all_teachers = get_all_teachers()

    return APIResponse.respond(data=all_teachers)


@principal_assignments_resources.route(
    "/assignments/grade", methods=["POST"], strict_slashes=False
)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    if assignment == None:
        return jsonify({"error": "FyleError"}), 404

    if assignment.state == AssignmentStateEnum.DRAFT:
        return jsonify({"error": "FyleError"}), 400

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p,
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
