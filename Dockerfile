# Use Python 3.8 slim runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install virtualenv and create a virtual environment
RUN pip install virtualenv
RUN virtualenv env --python=python3.8

# Activate the virtual environment and install dependencies
RUN . env/bin/activate
RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables
ENV FLASK_APP=core/server.py

# Remove any existing SQLite database (optional, for a fresh start)
RUN rm -f core/store.sqlite3

# Run Flask migrations
RUN flask db upgrade -d core/migrations/


# Expose the port the app runs on
EXPOSE 7755

# Command to start the server using a bash script
CMD ["bash", "run.sh"]
