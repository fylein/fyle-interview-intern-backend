# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask
ENV FLASK_APP=core/server.py

# Expose the port on which the Flask app will run

# I have chosen to use 7755 port as, it was the original port of the app in assignment
EXPOSE 7755

# Run app.py when the container launches
CMD ["bash", "run.sh"]
