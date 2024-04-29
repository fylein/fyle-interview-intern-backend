FROM python:3.8

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# en_IN UTF-8/en_IN UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone

ENV LANG en_IN.UTF-8
ENV LC_NUMERIC en_IN.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

## Set the FLASK_APP environment variable
ENV FLASK_APP=core/server.py

## Remove the core/store.sqlite3 file
RUN rm -f core/store.sqlite3

## Run the Flask db upgrade command
RUN flask db upgrade -d core/migrations/

## Add the run.sh script
COPY run.sh .
RUN chmod +x run.sh

## Expose the port
EXPOSE 7755

## Start the Flask app
CMD ["./run.sh"]