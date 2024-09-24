from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from core.models.teachers import Teacher

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True  # Automatically converts data into a Teacher instance
        include_fk = True  # Includes foreign key fields if necessary
        exclude = ('user_id',)  # Exclude 'user_id' if it's not needed
        load_only = ('id',)  # Only load 'id', don't dump it if necessary
        dump_only = ('created_at', 'updated_at')  # Only dump timestamps
