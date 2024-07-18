# The Official Python image from the Docker Hub
FROM python:3.8-slim

WORKDIR /app

# Copy application code into the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Reset the DB
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Expose the port the app runs on
EXPOSE 7755

# Run the Flask application
CMD ["bash", "run.sh"]