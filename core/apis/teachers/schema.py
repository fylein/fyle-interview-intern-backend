from marshmallow import EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    name = auto_field()
    email = auto_field()
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Teacher(**data_dict)
