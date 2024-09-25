from flask import jsonify
from models import Teacher
from core.decorators import principal_required

@principal_required
def list_all_teachers():
    teachers = Teacher.query.all()
    
    result = [teacher.to_dict() for teacher in teachers]
    return jsonify({"data": result}), 200
