from flask import Blueprint, jsonify
from models import User  # Assuming you have a User model
from decorators import principal_required  # Assuming you have a decorator for principal authentication

principal_teachers_blueprint = Blueprint('principal_teachers', __name__)

@principal_teachers_blueprint.route('/principal/teachers', methods=['GET'])
@principal_required
def list_teachers():
    teachers = User.query.filter_by(role='teacher').all()
    return jsonify({"data": [teacher.to_dict() for teacher in teachers]})
