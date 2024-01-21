# Instructions to start the application:
# 1. Use the Dockerfile present in current folder to create image in Docker. You can use the below command in the current folder:
## docker build -t fyle_interview_intern_backend_main .
### This will create Docker image with a name "fyle_interview_intern_backend_main" which should be accessible in your Docker app
# 2. Go to Docker app and navigate to Images section. Click triangle play button besides application name. Expand "Optional Settings" and input "7755" port in "Host Port" field under Port section.
# 3. Click run to create a new container and start the server. API will be running on http://localhost:7755/

#-----------------------------------------------------------------------------------------------------------

# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.8.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on(7755).
EXPOSE 7755

# to stop on first error
CMD set -e

# Run required migrations
CMD export FLASK_APP=core/server.py

# Run server
CMD gunicorn -c gunicorn_config.py core.server:app

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/
