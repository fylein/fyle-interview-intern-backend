from .exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

def base_assert(error_code, msg):
    raise FyleError(status_code=error_code, message=msg)


def assert_auth(cond, msg='UNAUTHORIZED'):
    if cond is False:
        base_assert(401, msg)


def assert_true(cond, msg='FORBIDDEN'):
    if cond is False:
        base_assert(403, msg)


def assert_valid(cond, msg='BAD_REQUEST'):
    if cond is False:
        base_assert(400, msg)


def assert_found(_obj, msg='NOT_FOUND'):
    if _obj is None:
        base_assert(404, msg)

def assert_validate(cond, msg='INVALID'):
    if(cond is False):
        raise ValidationError(message=msg)

def assert_integrity(cond, msg='Integrity Error'):
    if(cond is False):
        raise IntegrityError(msg, {}, None)