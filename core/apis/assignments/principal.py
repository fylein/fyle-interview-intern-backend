from flask import Blueprint,jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,Teacher,AssignmentStateEnum
from .schema import AssignmentSchema,TeacherSchema,AssignmentGradeSchema

# Creating a Blueprint variable for routing
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


# List all submitted and graded assignments
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
  """Returns list of graded and submitted assignments"""
  students_assignments = Assignment.get_graded_submitted_assignments()
  students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
  return APIResponse.respond(data=students_assignments_dump)

# List all the teachers
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teachers(p):
  """Returns list of teachers"""
  teachers = Teacher.query.all()
  teachers_dump = TeacherSchema().dump(teachers, many=True)
  return APIResponse.respond(data=teachers_dump)
  

# Grade or re-grade an assignment
@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def edit_grade_of_assignment(p,incoming_payload):
  """Grade or re-grade an assignment"""
  edit_grade_assignments_payload = AssignmentGradeSchema().load(incoming_payload)
  edited_graded_assignment=Assignment.mark_grade(
    _id=edit_grade_assignments_payload.id,
    grade=edit_grade_assignments_payload.grade,
    auth_principal=p 
  )
  db.session.commit()
  edited_graded_assignment_dump=AssignmentSchema().dump(edited_graded_assignment)
  return APIResponse.respond(data=edited_graded_assignment_dump)