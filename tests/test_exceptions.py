import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    error = FyleError(404, "Not Found")
    assert error.status_code == 404
    assert error.message == "Not Found"

def test_fyle_error_to_dict():
    error = FyleError(400, "Bad Request")
    error_dict = error.to_dict()
    assert error_dict == {'message': 'Bad Request'}

def test_fyle_error_default_status_code():
    error = FyleError(500, "Internal Server Error")
    assert error.status_code == 500
