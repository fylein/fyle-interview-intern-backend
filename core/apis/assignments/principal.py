from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema
from core.models.teachers import Teacher
from marshmallow import ValidationError
from flask import request
from core.models.assignments import AssignmentStateEnum
from core.libs import helpers, assertions


principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    principal_assignments = Assignment.get_all_submitted_and_graded_by_principal(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)



@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of Teacher"""
    teachers_list = Teacher.get_all_teachers()
    teachers_dict = [teacher.to_dict() for teacher in teachers_list]
    return APIResponse.respond(data=teachers_dict)    



@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def grade_assignment(p):
    """
    Grade or re-grade an assignment
    """
   
       
    payload = request.get_json()
    assignment_id = payload.get('id')
    grade = payload.get('grade')
        

        
        
    if not assignment_id or not grade:
        return APIResponse.respond_error('Missing required fields: id or grade', 400)


    assignment = Assignment.get_by_id(assignment_id)
    assertions.assert_found(assignment, 'No assignment with this id was found')
      
     
       
    updated_assignment = Assignment.mark_grade(
        _id=assignment_id, 
        grade=grade, 
        auth_principal=p
    )

       
    assignment_dump = AssignmentSchema().dump(updated_assignment)
        
    return APIResponse.respond(data=assignment_dump)

      
  
    


