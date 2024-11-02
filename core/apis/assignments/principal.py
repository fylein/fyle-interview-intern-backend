from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.principals import Principal
from core.libs.exceptions import FyleError
from flask import request
from core.models.assignments import AssignmentStateEnum
from core.libs import assertions
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of graded and submitted assignments"""
    # Check if principal_id is present in the principal table
    if p.principal_id is None:
        raise FyleError(message='Principal ID not found', status_code=400)
    
    if Principal.query.get(p.principal_id) is None:
        raise FyleError(message='Principal not found', status_code=400)
    
    principal_assignments = Assignment.query.filter(Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])).all()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)



@principal_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def regrade_assignment(p):
    """Regrades an assignment"""
    data = AssignmentGradeSchema().load(request.json)
    try:
        regraded_assignment=Assignment.re_grade(data.id, data.grade, p)
        print("regraded_assignment",regraded_assignment)
        db.session.commit()
        regraded_assignment_dump = AssignmentSchema().dump(regraded_assignment)

    except FyleError as e:
        db.session.rollback()
        raise e
    except Exception as e:

        db.session.rollback()
        message = {
            "data":{
                "state": AssignmentStateEnum.GRADED.value,
                "grade": data.grade
            },
            "message": str(e)
        }

        raise FyleError(message=message, status_code=400)
    
    return APIResponse.respond(data=regraded_assignment_dump)