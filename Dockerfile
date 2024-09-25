FROM python:3.8.0

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=core/server.py
RUN flask db upgrade -d core/migrations/

EXPOSE 7755

CMD ["pytest","--cov"]