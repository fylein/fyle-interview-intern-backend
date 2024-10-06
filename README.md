# Fyle Backend Challenge


## Docker Setup

To run this application with Docker, follow these steps:

1. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.
2. Build the Docker image:
   ```bash
   docker-compose build
3. Run the application:
   docker-compose up
4. The application will be accessible at http://localhost:5000




## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

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


