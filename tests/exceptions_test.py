# A new tests for expetions testing

from core.libs.exceptions import FyleError


def test_fyle_error_to_dict():
    try:
        raise FyleError(404, 'Not Found')
    except FyleError as e:
        error_dict = e.to_dict()
        assert 'message' in error_dict
        assert error_dict['message'] == 'Not Found'
        assert e.status_code == 404
