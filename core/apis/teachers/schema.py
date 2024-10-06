from marshmallow import Schema, fields

class TeacherSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()