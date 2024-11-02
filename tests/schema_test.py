from core.apis.assignments.schema import AssignmentGradeSchema, AssignmentSchema, AssignmentSubmitSchema
from core.models.assignments import Assignment, GradeEnum

def test_assignment_schema():
    assignment = Assignment(
        id=1,
        content='content',
        teacher_id=1,
        student_id=1,
        grade=GradeEnum.A,
        state=2
    )

    assignment_dump = AssignmentSchema().dump(assignment)
    assert assignment_dump['id'] == 1
    assert assignment_dump['content'] == 'content'
    assert assignment_dump['teacher_id'] == 1
    assert assignment_dump['student_id'] == 1
    assert assignment_dump['grade'] == GradeEnum.A
    assert assignment_dump['state'] == 2

    assignment_load = AssignmentSchema().load(assignment_dump)
    assert assignment_load.id == 1
    assert assignment_load.content == 'content'

def test_assignment_submit_schema():
    assignment_submit = {
        'id': 1,
        'teacher_id': 1
    }

    assignment_submit_dump = AssignmentSubmitSchema().dump(assignment_submit)
    assert assignment_submit_dump['id'] == 1
    assert assignment_submit_dump['teacher_id'] == 1

    assignment_submit_load = AssignmentSubmitSchema().load(assignment_submit_dump)
    assert assignment_submit_load.id== 1
    assert assignment_submit_load.teacher_id == 1
