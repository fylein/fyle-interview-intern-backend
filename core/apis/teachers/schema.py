from marshmallow import EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher
from core.libs.helpers import GeneralObject


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(dump_only=True)  # Primary key, read-only
    user_id = auto_field(required=True)  # Foreign key, required field
    created_at = auto_field(dump_only=True)  # Timestamp, read-only
    updated_at = auto_field(dump_only=True)  # Timestamp, read-only

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Teacher(**data_dict)


class TeacherCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE
        load_instance = True

    user_id = auto_field(required=True)  # Foreign key, required field

    @post_load
    def create_teacher(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)
