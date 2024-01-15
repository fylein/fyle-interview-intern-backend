FROM python:3.8

# seting the working dir and copying content to /app
WORKDIR /app
COPY . /app

#Installing packages
RUN pip install virtualenv
RUN virtualenv env --python=python3.8
RUN /bin/bash -c "source env/bin/activate && pip install --no-cache-dir -r requirements.txt"

#setting env variable
ENV FLASK_APP=core/server.py

# reseting database
RUN /bin/bash -c "source env/bin/activate && rm core/store.sqlite3 && flask db upgrade -d core/migrations/"

#exposing port
EXPOSE 5000

# Run the command to start the server
CMD ["bash", "run.sh"]

