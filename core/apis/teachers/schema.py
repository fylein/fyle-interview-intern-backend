from marshmallow import Schema, EXCLUDE,fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher

class TeacherSchema(Schema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    user_id = auto_field(dump_only=True)

    @post_load
    def make_teacher(self, data, **kwargs):
        return Teacher(**data)