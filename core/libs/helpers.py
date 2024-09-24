import random
import string
import json
from datetime import datetime
from functools import wraps
from flask import request
from core.libs.exceptions import FyleError

TIMESTAMP_WITH_TIMEZONE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class GeneralObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_utc_now():
    return datetime.utcnow()


# Decorator to ensure the user is a principal
def ensure_principal(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract 'X-Principal' header from the request
        principal_header = request.headers.get('X-Principal')

        if not principal_header:
            raise FyleError("Missing X-Principal header", 401)

        principal_data = None
        try:
            # Parse the header JSON to extract principal information
            principal_data = json.loads(principal_header)
        except ValueError:
            raise FyleError("Invalid X-Principal header", 400)

        # Check if the 'principal_id' is present in the header data
        if 'principal_id' not in principal_data:
            raise FyleError("Unauthorized. Principal access required.", 403)

        # Pass execution to the decorated route function
        return f(*args, **kwargs)

    return decorated_function
