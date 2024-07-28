# Fyle Backend

* #### Clone the repository
```
https://github.com/sanska-r-epo/fyle-interview-intern-backend.git
```
* #### Navigate to the project directory
```
cd fyle-interview-intern-backend
```
* #### Now proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
```
```
source env/bin/activate
```
```
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
```
```
rm core/store.sqlite3
```
```
flask db upgrade -d core/migrations/
```

## **Run Application** 

### Start Server

```
bash run.sh
```
### Access the application at http://localhost:7755

### Stop the application
` press Ctrl+C `

### Run Tests

```
pytest -vvv -s tests/
```

### For test coverage report
```
pytest --cov
```
```
open htmlcov/index.html
```

## **Build and Run Application with docker compose**

### Build the image

```
docker-compose -f docker-compose.build.yaml build
```

### Run the application

```
docker-compose -f docker-compose.run.yaml up
```
### Access the application at http://localhost:9999

### Stop the application
` press Ctrl+C ` and run bellow command
```
docker-compose -f docker-compose.run.yaml down
```