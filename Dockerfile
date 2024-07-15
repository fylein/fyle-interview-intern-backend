# Dockerfile
FROM python:3.10
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["bash", "run.sh"]