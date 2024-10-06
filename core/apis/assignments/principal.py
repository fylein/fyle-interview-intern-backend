from core import db
from flask import jsonify, request, Blueprint
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from sqlalchemy.exc import IntegrityError
from core import create_app  
import json
from json.decoder import JSONDecodeError 

app=create_app()

principal_blueprint = Blueprint('principal', __name__)
@principal_blueprint.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    
    x_principal = request.headers.get('X-Principal')
    
    if not x_principal:
        return jsonify(error="Missing X-Principal header"), 400

    try:
        principal_data = json.loads(x_principal)
        principal_id = principal_data['principal_id']
    except (KeyError, JSONDecodeError):
        return jsonify(error="Invalid X-Principal header"), 400

    assignments = Assignment.query.filter_by(principal_id=principal_id).all()
    
    

    if not assignments:
        return jsonify(data=[], message="No assignments found for this principal."), 404

    assignments_data = [assignment.serialize() for assignment in assignments]
    
    
    return jsonify(data=assignments_data), 200



assignmentgrading_blueprint = Blueprint('assignmentgrading', __name__)

@assignmentgrading_blueprint.route('/principal/assignments/grade', methods=['POST'])
def grade_assignment():
    
    if not request.is_json:
        return jsonify({'error': 'Invalid content type'}), 400
    
    
    x_principal = request.headers.get('X-Principal')
    
    
    if not x_principal:
        return jsonify(error="Missing X-Principal header"), 400

    try:
        principal_data = json.loads(x_principal)
        principal_id = principal_data.get('principal_id')
    except (KeyError, JSONDecodeError):
        return jsonify(error="Invalid X-Principal header"), 400

    data = request.json

    if not data and 'id' not in data and 'grade' not in data:
        return jsonify(error="Missing 'id' or 'grade' in the request"), 400


    if 'grade' not in data and 'id' in data:
        return jsonify(error="Missing 'grade' in the request"), 400


    if 'id' not in data:
        return jsonify(error="Missing 'id' in the request"), 400
    
    
    try:
        assignment = Assignment.query.get(data['id'])
        
     
        if not assignment:
            return jsonify(error="Assignment not found"), 404

        if assignment.state == AssignmentStateEnum.DRAFT:
            return jsonify({'error': 'Cannot grade an assignment in DRAFT state'}), 400

        if assignment.principal_id != principal_id:
            return jsonify(error="Unauthorized: Assignment does not belong to the principal"), 403
      
        

        if data['grade'] not in [grade.value for grade in GradeEnum]:  # Assuming GradeEnum is an enum with valid grades
            return jsonify(error="Invalid grade provided"), 400


        assignment.grade = data['grade']

        db.session.commit()  

        
        return jsonify(data=assignment.serialize()), 200


    except IntegrityError:
        db.session.rollback()  
        return jsonify(error="Database integrity error"), 500
    except Exception as e:
        db.session.rollback()  
        return jsonify(error=str(e)), 500