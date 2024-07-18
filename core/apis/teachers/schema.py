# core/schemas.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,auto_field
from core.models.teachers import Teacher

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        include_relationships = True
        load_instance = True

    user_id = auto_field(dump_only=True)