FROM python:3.10
## Set the FLASK_APP environment variable
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Remove the core/store.sqlite3 file
RUN rm -f core/store.sqlite3

## Run the Flask db upgrade command
RUN flask db upgrade -d core/migrations/

COPY . .
EXPOSE 5000
CMD ["bash", "run.sh"]
