from core.libs.exceptions import FyleError


def test_fyle_error():
    error = FyleError(404, 'page not found')
    assert error.status_code == 404
    assert error.message == 'page not found'


def test_fyle_error_to_dict():
    error = FyleError(404, 'page not found')
    error_dict = error.to_dict()
    assert isinstance(error_dict, dict)
    assert error_dict['message'] == 'page not found'