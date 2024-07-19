from core.libs.exceptions import FyleError


def test_FyleError_class():
    fyle_error = FyleError(404, 'Not Found')
    assert fyle_error.status_code == 404
    assert fyle_error.message == 'Not Found'


def test_FyleError_to_dict():
    fyle_error = FyleError(404, 'Not Found')
    fyle_error_dict = fyle_error.to_dict()
    assert isinstance(fyle_error_dict, dict)
    assert fyle_error_dict['message'] == 'Not Found'