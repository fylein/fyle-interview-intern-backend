# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port the application runs on
EXPOSE 7755

# Command to run the application
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
