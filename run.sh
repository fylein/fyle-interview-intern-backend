#!/bin/bash

# to stop on first error
set -e

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations
export FLASK_APP=core/server.py

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

FILE="core/store.sqlite3"
export FLASK_APP=core/server.py

# Check if the file exists
if [ -f "$FILE" ]; then
    rm "$FILE"
fi
flask db upgrade -d core/migrations/

# Run server
gunicorn -c gunicorn_config.py core.server:app