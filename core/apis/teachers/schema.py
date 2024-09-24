# teachers/schema.py
from marshmallow import Schema, fields

# Schema for the Assignment model
class PrincipalAssignmentSchema(Schema):
    id = fields.Int(required=True)
    content = fields.Str(required=True)
    grade = fields.Str(allow_none=True)
    state = fields.Str(required=True)
    student_id = fields.Int(required=True)
    teacher_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

# Schema for the Teacher model
class TeacherSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
