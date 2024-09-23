from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest

from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


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
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code
    return jsonify(
        error='GenericError',
        message=str(err)  # This will provide the message of the exception
    ), 500
    raise err

@app.route('/test/error')
def test_error_handler():
    exception_type = request.args.get('type')  # Get the type from query params
    if exception_type == 'FyleError':
        raise FyleError("Sample error", 400)
    elif exception_type == 'ValidationError':
        raise ValidationError({"field": ["error"]})
    elif exception_type == 'IntegrityError':
        raise IntegrityError("Integrity error", "some query", "params")
    elif exception_type == 'HTTPException':
        raise BadRequest("This is a bad request")    
    else:
        raise Exception("Unknown error")


@app.route('/test/generic-error')
def generic_error():
    raise Exception("This is a generic error")


    


