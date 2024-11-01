from core.models.users import User
from core import db
from sqlalchemy import text
import datetime

def test_create_user(db_session):

    user = User(id=90,username='test256',email='test256@gmail.com',created_at=datetime.datetime.now(),updated_at=datetime.datetime.now())
    db.session.add(user)
    db.session.commit()

    # Remove the user from the database
    db.session.delete(user)
    db.session.commit()
    
    assert user.id == 90
    assert user.username == 'test256'
    assert user.email == 'test256@gmail.com'

    