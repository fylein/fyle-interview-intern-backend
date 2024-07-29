FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9999

ENV FLASK_APP core/server.py

CMD ["flask", "run", "--host=0.0.0.0"]
