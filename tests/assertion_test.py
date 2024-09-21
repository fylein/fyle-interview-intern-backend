from core.libs import assertions
from core.libs.exceptions import FyleError


def test_assert_auth():
    try:
        assertions.assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'


def test_assert_true():
    try:
        assertions.assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'


def test_assert_valid():
    try:
        assertions.assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400


def test_assert_found():
    try:
        assertions.assert_found(None)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'