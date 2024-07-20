from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
import os

app = Flask(__name__)
# Use environment variables for configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///./store.sqlite3')
app.config['SQLALCHEMY_ECHO'] = False if os.getenv('SQLALCHEMY_ECHO') == 'False' else True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False if os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'False' else True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        try:
            with dbapi_connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys=ON;")
        except Exception as e:
            app.logger.error(f"Error setting PRAGMA foreign_keys=ON on SQLite connection: {e}")

# Add other initializations if needed