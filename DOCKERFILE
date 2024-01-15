# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install virtualenv
RUN virtualenv env --python=python3.8

RUN . env/bin/activate
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=core/server.py

# Remove the SQLite database
RUN test -f core/store.sqlite3 && rm core/store.sqlite3 || true

# Upgrade the database
RUN flask db upgrade -d core/migrations/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the command to start the server
CMD ["bash", "run.sh"]
