# Fyle Backend Challenge completed ✅

### Development env: 
> Ubuntu 22.04 LTS
> 
>  python3.8.19

cd fyle-interview-intern-backend

virtualenv fylenv --python=python3.8
. fylenv/bin/activate

pip install -r requirements.txt
```

### Run tests using this cmd.
```
# reset DB
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
# lets see
pytest -vvv -s tests/
```

### Start Server

```
# first reset DB
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
# then lets go
bash run.sh
```

### view the test coverage in the browser using this cmd.
```
# first reset DB
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
# lets go
pytest --cov --cov-report html
open htmlcov/index.html
```

### Build the docker container first using this cmd.
this cmd is meant to be used when you made some changes or building first time. open your docker desktop first to start the docker engine and then enter the following cmd
```
docker compose up --build -d
```

### Run docker container using this cmd.
```
docker compose up -d
```

### Shut docker container up using this cmd.
```
docker compose down
```
