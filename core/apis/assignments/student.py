from flask import Blueprint
from flask import jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
@@ -22,6 +23,9 @@ def list_assignments(p):
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    if 'content' not in incoming_payload or incoming_payload['content'] is None:
        return jsonify({'error': 'Content cannot be null'}), 400

    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

@@ -38,11 +42,24 @@ def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
    try:
        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth_principal=p
        )
        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
        return APIResponse.respond(data=submitted_assignment_dump)

    except ValueError as e:
        return APIResponse.respond_with_error('FyleError', str(e), 400)

    # submitted_assignment = Assignment.submit(
    #     _id=submit_assignment_payload.id,
    #     teacher_id=submit_assignment_payload.teacher_id,
    #     auth_principal=p
    # )
    # db.session.commit()
    # submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    # return APIResponse.respond(data=submitted_assignment_dump)
