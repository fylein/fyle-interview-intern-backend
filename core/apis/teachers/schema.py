from marshmallow import EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields
from core.models.teachers import Teacher
from core.models.users import User  # Import the User model


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['id']
        unknown = EXCLUDE

    username = auto_field()
    email = auto_field()
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(required=False, allow_none=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)

    user_id = auto_field()

    # Change this to use the user relationship instead of user_id
    user_details = fields.Nested(UserSchema, attribute="user", dump_only=True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        # Optional: Perform additional validation if necessary
        return Teacher(**data_dict)
