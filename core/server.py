from flask import jsonify, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_assigment_resources
from core.apis.teachers import principal_teacher_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Saniya/Projects/InternshipProject/Fyle_permission_project/fyle-interview-intern-backend/core/store.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optionally turn off modification tracking to save resources

# Initialize the database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_teacher_resources, url_prefix='/principal/teachers')
app.register_blueprint(principal_assigment_resources, url_prefix='/principal/assignments')


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

    raise err
