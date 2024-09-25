FROM python:3.8.0

WORKDIR /code

ENV FLASK_APP=core/server.py

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN flask db upgrade -d core/migrations/

EXPOSE 7755

CMD ["/bin/bash", "-c", "pytest --cov && coverage html && bash run.sh"]