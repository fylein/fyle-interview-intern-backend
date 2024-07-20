from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher  # Adjust import based on your project structure

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field()
    subject = auto_field()
