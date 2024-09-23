# Using Python's official minimal image
FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt .
# Install dependencies
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=core/server.py
# Run the database migrations
RUN flask db upgrade -d core/migrations/

CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]