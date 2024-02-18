# Use a more specific Python runtime as a parent image
FROM python:3.8-slim-buster

# Create a non-root user
RUN useradd -m myuser
USER myuser

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt initially to leverage Docker caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=core/server.py

# Expose the port on which the Flask app will run
EXPOSE 7755

# Run run.sh when the container launches
CMD ["bash", "run.sh"]
