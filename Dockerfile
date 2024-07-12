FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./run.sh" ]
