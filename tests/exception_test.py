import pytest
from core.libs.exceptions import FyleError


def test_fyle_error_init():
    error_message = 'Test error message'
    error_status_code = 400

    fyle_error = FyleError(error_status_code, error_message)

    assert fyle_error.message == error_message
    assert fyle_error.status_code == error_status_code


def test_fyle_error_to_dict():
    error_message = 'Test error message'
    error_status_code = 400

    fyle_error = FyleError(error_status_code, error_message)
    error_dict = fyle_error.to_dict()

    assert error_dict['message'] == error_message
