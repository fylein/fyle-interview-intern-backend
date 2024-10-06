from flask import jsonify, request, Blueprint
from core.models.teachers import Teacher
from core import create_app  
import json
from json.decoder import JSONDecodeError 

app=create_app()

principalteacher_blueprint = Blueprint('principalteacher', __name__)



@principalteacher_blueprint.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    x_principal = request.headers.get('X-Principal')

    if not x_principal:
        return jsonify(error="Missing X-Principal header"), 400

    try:
        principal_data = json.loads(x_principal)
        principal_id = principal_data['principal_id']

        if not isinstance(principal_id, int) or principal_id <= 0:
            return jsonify(error="Invalid principal_id"), 400

    except (KeyError, json.JSONDecodeError):
        return jsonify(error="Invalid X-Principal header"), 400

    teachers = Teacher.query.filter_by(principal_id=principal_id).all()

    
    if not teachers:
        return jsonify(data=[], message="No teachers found for this principal."), 404

    
    teachers_data = [teacher.serialize() for teacher in teachers]

    return jsonify(data=teachers_data), 200

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500