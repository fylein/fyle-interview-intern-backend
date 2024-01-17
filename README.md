# Docker Setup
### Steps to build and run the application with Docker
* Go to folder containing ```Dockerfile```
    * ```ls``` or ```dir```
    * If the list contains: ```Dockerfile```, go to the next step.
    * Else: ```cd fyle```
* Build the Docker Image:
  ```docker build -t my-flask-app .```
    * You can name it anything you want. Replace ```my-flask-app``` with your name, but use that name with rest of the steps.
* Run the Docker Container: ```docker run -p 7755:7755 my-flask-app```
* Congrats! You can access the flask app with: ```http://localhost:7755```


# Pytest:
### Result from ```pytest tests/```
![Screenshot (214)](https://github.com/lklivingstone/fyle-interview-intern-backend/assets/74340009/879caa41-5f3a-4dd1-ae8d-d230a7107a81)

### Test Coverage:
#### The test covers **99%**
![Screenshot (209)](https://github.com/lklivingstone/fyle-interview-intern-backend/assets/74340009/28c63e9e-db21-4a40-b274-d5baec0ec754)

The **1%** is lost due to the decorator.py which cannot be covered.
![Screenshot (210)](https://github.com/lklivingstone/fyle-interview-intern-backend/assets/74340009/91af125d-ec09-41e9-9286-b4d56e9215c4)


# Github Artifacts
#### I have enabled GitHub Actions through which you can do the following:
* **flake8 linting**
* **black check**
* **Pytest Coverage which can be downloaded as Artifacts (zip file)**

### Coverage Artifact:
![Screenshot (213)](https://github.com/lklivingstone/fyle-interview-intern-backend/assets/74340009/888851fe-9caa-4202-b340-c3c100f8a478)

### Flake8 and Black Lint:
![Screenshot (212)](https://github.com/lklivingstone/fyle-interview-intern-backend/assets/74340009/b66273fa-ec34-4361-a4d9-fbad048fc18d)


# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to intern at Fyle and work with our engineering team. You should be able to commit to at least 6 months of dedicated time for internship.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

This challenge involves writing a backend service for a classroom. The challenge is described in detail [here](./Application.md)


## What happens next?

You will hear back within 48 hours from us via email. 


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
