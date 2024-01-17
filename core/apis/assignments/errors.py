from flask import Blueprint
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import abort

errors_resources = Blueprint("errors_resources", __name__)


@errors_resources.route("/simulate_validation_error")
def simulate_validation_error():
    raise ValidationError("Validation error")


@errors_resources.route("/simulate_integrity_error")
def simulate_integrity_error():
    raise IntegrityError("Integrity error", params=None, orig=None)


@errors_resources.route("/simulate_http_exception")
def simulate_http_exception():
    abort(404)


@errors_resources.route("/simulate_unhandled_error")
def simulate_unhandled_error():
    raise Exception("Unhandled error")
