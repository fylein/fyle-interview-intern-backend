FROM python:3.8
WORKDIR /app
COPY . /app

RUN pip install virtualenv
RUN virtualenv env --clear --python=python3.8
RUN /bin/bash -c "source env/bin/activate"
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=core/server.py
CMD [ "bash","run.sh" ]