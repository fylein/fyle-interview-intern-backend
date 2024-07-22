import pytest
from core.libs.exceptions import FyleError


def test_fyle_error_initialization():
    error = FyleError(status_code=404, message="Not Found")
    assert error.status_code == 404
    assert error.message == "Not Found"

def test_fyle_error_default_status_code():
    error = FyleError(status_code=400, message="Bad Request")
    assert error.status_code == 400
    assert error.message == "Bad Request"

def test_fyle_error_to_dict():
    error = FyleError(status_code=500, message="Internal Server Error")
    error_dict = error.to_dict()
    assert error_dict['message'] == "Internal Server Error"

def test_fyle_error_raises_exception():
    with pytest.raises(FyleError) as excinfo:
        raise FyleError(status_code=403, message="Forbidden")
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == "Forbidden"
