from flask import jsonify
from marshmallow.exceptions import ValidationError
from core.apis.assignments.principal import principal_blueprint, assignmentgrading_blueprint
from core.apis.teachers.principal import principalteacher_blueprint
from core import create_app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError

app = create_app()

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_blueprint)
app.register_blueprint(principalteacher_blueprint)
app.register_blueprint(assignmentgrading_blueprint)

@app.route('/')
def home():
    return jsonify(message="App is running"), 200



@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message="Integrity constraint violation"
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err


if __name__ == "__main__":
    app.run(debug=True)