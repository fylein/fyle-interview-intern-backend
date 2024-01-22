FROM python:3.8.18-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
COPY . ./app
EXPOSE 7755
RUN export FLASK_APP=core/server.py
RUN rm core/store.sqlite3
RUN flask db upgrade -d core/migrations/
CMD ['bash'', 'run.sh]