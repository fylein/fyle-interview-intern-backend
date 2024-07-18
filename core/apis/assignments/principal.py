from flask import Blueprint, jsonify
from models import Assignment  # Assuming you have an Assignment model
from decorators import principal_required

principal_assignments_blueprint = Blueprint('principal_assignments', __name__)

@principal_assignments_blueprint.route('/principal/assignments', methods=['GET'])
@principal_required
def list_assignments():
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    return jsonify({"data": [assignment.to_dict() for assignment in assignments]})
