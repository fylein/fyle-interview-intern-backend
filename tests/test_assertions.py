# Feature: Tests to increase test coverage for assertions.py
from core.libs import assertions
from core.libs.exceptions import FyleError


def test_assert_auth():
    # Test when condition is True
    assertions.assert_auth(True)  # Should not raise an error
    # Test when condition is False
    try:
        assertions.assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'


def test_assert_true():
    # Test when condition is True
    assertions.assert_true(True)  # Should not raise an error
    # Test when condition is False
    try:
        assertions.assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'


def test_assert_valid():
    # Test when condition is True
    assertions.assert_valid(True)  # Should not raise an error
    # Test when condition is False
    try:
        assertions.assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400


def test_assert_found():
    # Test when object is found
    obj = "test"
    assertions.assert_found(obj)  # Should not raise an error
    # Test when object is not found
    try:
        assertions.assert_found(None)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'