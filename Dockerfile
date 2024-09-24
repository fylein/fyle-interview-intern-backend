FROM python:3.8-slim

# Set the working directory in the container and copy the contents
WORKDIR /app
COPY . /app

# Configuring virtual environment
RUN pip install virtualenv
RUN virtualenv env --python=python3.8

# Activate the virtual environment and install dependencies
RUN . env/bin/activate  
RUN  pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Remove any existing SQLite database and run db migrations
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Expose the port 
EXPOSE 7755

# Command to start the server using a bash script
CMD ["bash", "run.sh"]