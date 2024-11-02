FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=core/server.py

EXPOSE 5000

RUN chmod +x run.sh

CMD ["./run.sh"]