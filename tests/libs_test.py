# /tests/libs_test.py
import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found, base_assert
from core.libs.exceptions import FyleError

# Tests for assertions.py
def test_assert_auth():
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False, "Unauthorized error")
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == "Unauthorized error"
    
    # Test when the condition is True
    assert_auth(True, "This should not raise")

def test_assert_true():
    with pytest.raises(FyleError) as excinfo:
        assert_true(False, "Forbidden error")
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == "Forbidden error"
    
    # Test when the condition is True
    assert_true(True, "This should not raise")

# Tests for exceptions.py
def test_fyle_error_initialization():
    error = FyleError(status_code=400, message="A Fyle error occurred")
    assert error.status_code == 400
    assert error.message == "A Fyle error occurred"

def test_fyle_error_to_dict():
    error = FyleError(status_code=400, message="A Fyle error occurred")
    error_dict = error.to_dict()
    assert error_dict['message'] == "A Fyle error occurred"