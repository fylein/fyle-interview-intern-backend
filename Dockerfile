# Python version 3.8 runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Starting environment and installing packages specified in requirements.txt
RUN pip install virtualenv
RUN virtualenv env --python=python3.8
RUN . env/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Resetting DB
RUN rm core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Expose the port the app runs on
EXPOSE 7755

# Run app.py when the container launches
CMD ["bash", "run.sh"]
