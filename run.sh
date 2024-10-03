#!/bin/bash

# Stop on the first error
set -e

# Delete older .pyc files, skipping the virtual environments
find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Set the FLASK_APP environment variable for Flask
export FLASK_APP=core/server.py

# Run required migrations if needed
# Uncomment if you're doing migrations manually
# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run the server with Gunicorn
# gunicorn -c gunicorn_config.py core.server:app
flask run