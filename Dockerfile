# Use an official Python runtime as a parent image
FROM python:3.8.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /fyle-interview-intern-backend

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Set Flask app environment variable
ENV FLASK_APP=core/server.py

# Remove the SQLite database file
RUN rm core/store.sqlite3

# Perform database migrations
RUN flask db upgrade -d core/migrations/

# Expose port 7755 for the Flask development server
EXPOSE 7755

