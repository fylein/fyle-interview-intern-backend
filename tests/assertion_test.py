from core.libs.exceptions import FyleError
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found
import pytest


def test_base_assert():
    # Test base_assert function
    try:
        base_assert(500, "Internal Server Error")
    except FyleError as e:
        assert e.status_code == 500
        assert e.message == "Internal Server Error"


def test_assert_auth():
    # Test assert_auth function with a true condition
    assert_auth(True)  # No exception should be raised

    # Test assert_auth function with a false condition
    with pytest.raises(FyleError) as e:
        assert_auth(False, "Custom Unauthorized Message")
    assert e.value.status_code == 401
    assert e.value.message == "Custom Unauthorized Message"


# Example for assert_true


def test_assert_true():
    assert_true(True)  # No exception should be raised

    with pytest.raises(FyleError) as e:
        assert_true(False, "Custom Forbidden Message")
    assert e.value.status_code == 403
    assert e.value.message == "Custom Forbidden Message"

# Example for assert_valid


def test_assert_valid():
    assert_valid(True)  # No exception should be raised

    with pytest.raises(FyleError) as e:
        assert_valid(False, "Custom Bad Request Message")
    assert e.value.status_code == 400
    assert e.value.message == "Custom Bad Request Message"

# Example for assert_found


def test_assert_found():
    obj = "example"  # An example object
    assert_found(obj)  # No exception should be raised

    with pytest.raises(FyleError) as e:
        assert_found(None, "Custom Not Found Message")
    assert e.value.status_code == 404
    assert e.value.message == "Custom Not Found Message"
