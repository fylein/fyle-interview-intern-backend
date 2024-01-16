# python image
FROM python:3.8-slim

# copy every content from the local file to the image
COPY . /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt


# Set environment variables
ENV FLASK_APP=core/server.py

# Remove the SQLite database
RUN rm core/store.sqlite3

# Run flask db upgrade
RUN flask db upgrade -d core/migrations/

# Expose the port the app runs on
EXPOSE 7755

# start the app
CMD ["bash", "run.sh"]