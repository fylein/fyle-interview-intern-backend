import pytest
import json
from core import db, create_app
from tests import app
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from core.config import get_sqlite_uri


@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture(scope='session')
def db_engine():

    engine = create_engine("sqlite:///myfile.db")

    # Listener to disable automatic transaction management
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        dbapi_connection.isolation_level = None

    # Listener to explicitly begin transactions
    @event.listens_for(engine, "begin")
    def do_begin(conn):
        conn.execute("BEGIN")

    yield engine
    engine.dispose()

@pytest.fixture(scope='function')
def db_session(db_engine):
    print('Creating a new session')



    Session = sessionmaker(bind=db_engine)
    session = Session()

    yield session  

    session.rollback()
    session.close()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers
