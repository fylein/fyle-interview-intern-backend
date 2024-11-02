from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs import assertions
from core.libs.exceptions import FyleError
from flask import request
from .schema import AssignmentSchema, AssignmentSubmitSchema
from core.models.assignments import AssignmentStateEnum
from core.models.teachers import Teacher

student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""

    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    try:
        if incoming_payload.get('id'):
            assignment = Assignment.get_by_id(incoming_payload.get('id'))
            assertions.assert_valid(assignment.student_id == p.student_id, 'This assignment belongs to some other student')
        
        else:
            assert 'teacher_id' in incoming_payload, 'teacher_id is required'
            if Teacher.query.get(incoming_payload['teacher_id']) is None:
                raise FyleError(message='Teacher not found', status_code=400)
            assignment = Assignment(student_id=p.student_id, teacher_id=p.teacher_id, content=incoming_payload['content'], state=AssignmentStateEnum.DRAFT)
    
        if not incoming_payload['content']:
            raise FyleError(message='Content cannot be empty', status_code=400)

        upserted_assignment = Assignment.upsert(assignment)
        db.session.commit()
        upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)

    except FyleError as e:
        db.session.rollback()
        raise e
    except Exception as e:
        db.session.rollback()
        raise FyleError(message=str(e), status_code=400)
    
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    
    try:
        submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
        assignment = Assignment.get_by_id(submit_assignment_payload.id)
        assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT, 'only a draft assignment can be submitted')
        assertions.assert_valid(assignment.student_id == p.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.teacher_id == submit_assignment_payload.teacher_id, 'This assignment belongs to some other teacher')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
       
        submitted_assignment = Assignment.submit(
            _id=submit_assignment_payload.id,
            teacher_id=submit_assignment_payload.teacher_id,
            auth_principal=p
        )
        db.session.commit()
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)

    except FyleError as e:
        db.session.rollback()
        raise e
    
    except Exception as e:
        db.session.rollback()
        raise FyleError(message=str(e)[:-1], status_code=400)
    
    return APIResponse.respond(data=submitted_assignment_dump)