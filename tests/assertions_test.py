from core.libs.assertions import assert_found, assert_valid, assert_true, assert_auth   
from core.libs.exceptions import FyleError

def test_assertions():
    try:
        assert_found(False)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'
        assert e.to_dict() == {'message': 'NOT_FOUND'}

    try:
        assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400
        assert e.message == 'BAD_REQUEST'
        assert e.to_dict() == {'message': 'BAD_REQUEST'}

    try:
        assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'
        assert e.to_dict() == {'message': 'FORBIDDEN'}
    
    try:
        assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'
        assert e.to_dict() == {'message': 'UNAUTHORIZED'}
