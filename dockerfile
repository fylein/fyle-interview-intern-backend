FROM python:3.8

WORKDIR /fyle_app

COPY . /fyle_app

RUN pip install virtualenv
RUN virtualenv myenv --python=python3.8

RUN /bin/bash -c "source myenv/bin/activate && pip install --no-cache-dir -r requirements.txt"

EXPOSE 7755

ENV FLASK_APP=core/server.py

CMD ["/bin/bash", "-c", "source myenv/bin/activate && bash run.sh"]
