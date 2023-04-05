from core import db
from core.models.users import User

def test_user_model_filter():
    # Test that filter method returns a query object
    result = User.filter()
    assert isinstance(result, db.Query)

def test_user_model_get_by_id():
    # Test that get_by_id method returns the correct user object
    user = User(username='test_user', email='test_user@example.com')
    db.session.add(user)
    db.session.commit()
    result = User.get_by_id(user.id)
    assert result == user

def test_user_model_get_by_email():
    # Test that get_by_email method returns the correct user object
    user = User(username='test_user2', email='test_user2@example.com')
    db.session.add(user)
    db.session.commit()
    result = User.get_by_email(user.email)
    assert result == user
# pytest --cov=core --cov-report html:htmlcov tests/