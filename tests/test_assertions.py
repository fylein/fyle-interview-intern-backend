import pytest
from core.libs.assertions import (
    base_assert,
    assert_auth,
    assert_true,
    assert_valid,
    assert_found
)
from core.libs.exceptions import FyleError

def test_base_assert_raises_fyle_error():
    with pytest.raises(FyleError) as exc_info:
        base_assert(400, "Test Error Message")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Test Error Message"

def test_assert_auth_raises_fyle_error():
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False, "Unauthorized Access")
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Unauthorized Access"

def test_assert_auth_passes():
    try:
        assert_auth(True)
    except FyleError:
        pytest.fail("assert_auth raised FyleError unexpectedly!")

def test_assert_true_raises_fyle_error():
    with pytest.raises(FyleError) as exc_info:
        assert_true(False, "Forbidden Access")
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "Forbidden Access"

def test_assert_true_passes():
    try:
        assert_true(True)
    except FyleError:
        pytest.fail("assert_true raised FyleError unexpectedly!")

def test_assert_valid_raises_fyle_error():
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False, "Bad Request Error")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Bad Request Error"

def test_assert_valid_passes():
    try:
        assert_valid(True)
    except FyleError:
        pytest.fail("assert_valid raised FyleError unexpectedly!")

def test_assert_found_raises_fyle_error():
    with pytest.raises(FyleError) as exc_info:
        assert_found(None, "Object Not Found")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "Object Not Found"

def test_assert_found_passes():
    try:
        assert_found("Some Object")  
    except FyleError:
        pytest.fail("assert_found raised FyleError unexpectedly!")
