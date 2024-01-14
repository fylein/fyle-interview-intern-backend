# server.py

from flask import Flask
from flask.cli import with_appcontext

def create_app():
    app = Flask(__name__)
    # ... other configuration

    @app.cli.command("init-db")
    @with_appcontext
    def init_db_command():
        # Implement your database initialization logic here
        # This could include creating tables, seeding initial data, etc.
        print("Initialized the database.")

    return app
