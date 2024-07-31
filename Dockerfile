# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies directly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=core/server.py

# Reset the database and run migrations
RUN rm -f core/store.sqlite3

RUN flask db upgrade -d core/migrations/

RUN rm -rf .pytest_cache

# Expose the port the app runs on
EXPOSE 7755

# Define the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:7755", "core.server:app"]
