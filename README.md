# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to intern at Fyle and work with our engineering team. You should be able to commit to at least 6 months of dedicated time for internship.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

**You are allowed to use any online/AI tool such as ChatGPT, Gemini, etc. to complete the challenge. However, we expect you to fully understand the code and logic involved.**

This challenge involves writing a backend service for a classroom. The challenge is described in detail [here](./Application.md)


## What happens next?

You will hear back within 48 hours from us via email. 


## **_Installation_**

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