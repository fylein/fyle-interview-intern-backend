FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7755

ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GUNICORN_PORT=7755

CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]