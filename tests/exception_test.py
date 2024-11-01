from core.libs.exceptions import FyleError

def test_exception():
    try:
        raise FyleError(400, 'BAD_REQUEST')
    except FyleError as e:
        assert e.status_code == 400
        assert e.message == 'BAD_REQUEST'
        assert e.to_dict() == {'message': 'BAD_REQUEST'}