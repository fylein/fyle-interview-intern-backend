from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_enum import EnumField
from core.models.assignments import Assignment, GradeEnum
from core.libs.helpers import GeneralObject


class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
@@ -49,3 +48,9 @@ class Meta:
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)

class TeacherSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
