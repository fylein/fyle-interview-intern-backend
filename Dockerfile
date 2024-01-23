FROM python:3.8
WORKDIR /app
COPY ./requirements.txt /app/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7755

ENV FLASK_APP=/app/core/server.py
# RUN test -e core/store.sqlite3 && rm core/store.sqlite3 || true \
    # && flask db upgrade -d /app/core/migrations/

CMD ["bash", "run.sh"]