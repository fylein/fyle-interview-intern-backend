from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher
from marshmallow import EXCLUDE


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    created_at = auto_field(dump_only=True)
    id = auto_field(required=False, allow_none=True)
    updated_at = auto_field(dump_only=True)
    user_id = auto_field(dump_only=True)
