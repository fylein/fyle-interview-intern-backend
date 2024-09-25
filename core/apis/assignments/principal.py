from flask import jsonify, request
from core.models import Assignment  # Assuming models.py contains Assignment model
from core.apis.decorators import principal_required
from core import db
from flask import Blueprint
from core.server import app

principal_assignments_resources = Blueprint('principal_assignments', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'])
def list_assignments():
    # Logic to list all assignments
    assignments = Assignment.query.all()  
    return jsonify({'data': assignments})

@app.route('/principal/assignments', methods=['GET'])
def list_all_assignments():
    # Authenticate principal
    principal = authenticate_principal(request.headers.get('X-Principal'))

    if not principal:
        return jsonify({"error": "Unauthorized"}), 403

    # Fetch all assignments (submitted or graded)
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()

    # Return the data
    return jsonify({
        "data": [assignment.to_dict() for assignment in assignments]
    })


@principal_required  # Ensure only the principal can access this route
def list_all_assignments():
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()

    result = [assignment.to_dict() for assignment in assignments]
    return jsonify({"data": result}), 200


@principal_required
def regrade_assignment():
    data = request.get_json()
    assignment_id = data.get('assignment_id')
    new_grade = data.get('new_grade')

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    assignment.grade = new_grade
    assignment.state = 'GRADED'
    db.session.commit()

    return jsonify({"data": assignment.to_dict()}), 200
