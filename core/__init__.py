from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./store.sqlite3'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.test_client()
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

@app.route('/hello', methods=['GET'])
def hello():
    """
    This is an example endpoint.
    ---
    responses:
      200:
        description: A successful response
    """
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)




# this is to enforce fk (not done by default in sqlite3)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
