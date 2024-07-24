from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException


app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')

app.register_blueprint(principal_assignments_resources, url_prefix='/principal')

@app.route('/')
def ready():