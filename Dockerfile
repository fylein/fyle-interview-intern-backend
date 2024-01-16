# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment and activate it
RUN /bin/bash -c "virtualenv env --python=python3.8 & source env/bin/activate & pip install --no-cache-dir -r requirements.txt"

# Make port 7755 available to the world outside this container
EXPOSE 7755

# Run run.sh when the container launches
CMD ["bash", "run.sh"]