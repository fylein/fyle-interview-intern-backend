# Feature: Added tests for validating exceptions.py
from core.libs.exceptions import FyleError


def test_fyle_error():
    error = FyleError(404, 'Not Found')
    assert error.status_code == 404
    assert error.message == 'Not Found'


def test_fyle_error_to_dict():
    error = FyleError(404, 'Not Found')
    error_dict = error.to_dict()
    assert isinstance(error_dict, dict)
    assert error_dict['message'] == 'Not Found'