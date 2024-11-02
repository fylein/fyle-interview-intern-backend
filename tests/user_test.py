from core.models.users import User
from core import db
from sqlalchemy import text
import datetime


def test_create_user():
    user = User(
        id=90,
        username="test256",
        email="test256@gmail.com",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.session.add(user)
    db.session.commit()
    assert user.id == 90
    assert user.username == "test256"
    assert user.email == "test256@gmail.com"

    # Remove the user from the database
    db.session.delete(user)
    db.session.commit()


def test_filter_user():
    criterion = User.id == 1
    user = User.filter(criterion).first()
    assert user.id == 1


def test_get_user_by_id():
    user = User.get_by_id(1)
    assert user.id == 1


def test_get_user_by_email():
    user = User.get_by_email("student1@fylebe.com")
    assert user.id == 1


def test_user_repr():
    user = User.query.get(1)
    assert user.__repr__() == "<User %r>" % user.username
