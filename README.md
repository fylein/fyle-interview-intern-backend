## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### To run the project locally, follow the steps below:

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

### Format Code

```
python -m black ./ 
```

### Lint Code

```
ruff check --fix
```

## To run the project in docker, follow the steps below:

### Build Docker Image

```
docker build -t fyle-intern-backend .
```

### Run Docker Container

```
docker run -d --name fyle-intern-backend-container -p 5000:5000 fyle-intern-backend
```

### Run Tests

```
ocker exec fyle-intern-backend-container pytest --cov -vvv -s tests/
```

### Format Code

```
docker exec fyle-intern-backend-container python -m black . --check
```

### Lint Code

```
docker exec fyle-intern-backend-container ruff check . --fix
```

### Stop and Remove Docker Container

```
docker stop fyle-intern-backend-container
docker rm fyle-intern-backend-container
```

