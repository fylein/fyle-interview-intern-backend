FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=core/server.py

RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

EXPOSE 7755

CMD ["bash", "run.sh"]