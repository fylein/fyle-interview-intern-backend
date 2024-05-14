from flask import Blueprint, jsonify
from core.apis.decorators import authenticate_principal
from core.models.assignments import Assignment
from core.apis.responses import APIResponse
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.apis import decorators

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)


@principal_assignments_resources.route("/assignments", methods=["GET"])
@authenticate_principal
def list_principal_assignments(principal):
    # print(principal.user_id, principal.principal_id)
    # Query the database to retrieve submitted and graded assignments for the principal
    assignments = Assignment.get_submitted_and_graded_assignments_for_principal(
        principal.user_id, principal.principal_id
    )
    # print(assignments)
    # Serialize the retrieved assignments into the desired JSON format
    assignment_schema = AssignmentSchema(many=True)
    assignments_data = assignment_schema.dump(assignments)

    # Return the serialized assignments as the response
    return APIResponse.respond(data=assignments_data)


@principal_assignments_resources.route("/teachers", methods=["GET"])
@authenticate_principal
def list_principal_teachers(principal):
    # Fetch all teachers
    teachers = Assignment.get_all_teachers()

    # Serialize the teachers into the desired JSON format
    teachers_data = [
        {
            "id": teacher.id,
            "user_id": teacher.user_id,
            "created_at": teacher.created_at.isoformat(),
            "updated_at": teacher.updated_at.isoformat(),
        }
        for teacher in teachers
    ]

    # Return the serialized teachers as the response
    return jsonify(data=teachers_data)


@principal_assignments_resources.route("/assignments/grade", methods=["POST"])
@decorators.accept_payload
@decorators.authenticate_principal
def regrade_assignment(principal, incoming_payload):
    # Extract assignment ID and grade from the request payload
    payload = AssignmentGradeSchema().load(incoming_payload)
    assignment_id = payload.id
    grade = payload.grade

    # Grade or re-grade the assignment
    graded_assignment = Assignment.grade_assignment(
        assignment_id, grade, principal.user_id, principal.principal_id
    )

    # Construct the response data
    assignment_data = {
        "content": graded_assignment.content,
        "created_at": graded_assignment.created_at.isoformat(),
        "grade": graded_assignment.grade,
        "id": graded_assignment.id,
        "state": graded_assignment.state.value,
        "student_id": graded_assignment.student_id,
        "teacher_id": graded_assignment.teacher_id,
        "updated_at": graded_assignment.updated_at.isoformat(),
    }

    # Return the graded assignment in the response
    return APIResponse.respond(data=assignment_data)