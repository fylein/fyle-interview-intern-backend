#!/bin/bash

export FLASK_APP=core/server.py
# Remove the SQLite database
rm core/store.sqlite3

# Apply database migrations
flask db upgrade -d core/migrations/

# Run pytest for tests
#pytest -vvv -s tests/
coverage run -m pytest tests/
coverage report -m
coverage html
