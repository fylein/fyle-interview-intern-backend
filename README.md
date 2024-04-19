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
### Installing Docker
1.	Install docker application
### Creating Docker file
2. Create a docker file with name `dockerfile` without any extension
3. Add
```
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Copy the entire local directory into the image
COPY . /app

# Activate virtual environment and install dependencies
RUN pip install -r requirements.txt
EXPOSE 4040
# Run bash script
CMD ["bash", "run.sh"]
```
in the dockerfile.
### Modifying run.sh
4. Open run.sh file and uncomment line 
```
# flask db upgrade -d core/migrations/
```
### Installing Ubuntu terminal and starting server
4. Install Ubuntu terminal and Run ` sudo apt-get install dos2unix` in ubuntu terminal
6. Run `sudo apt-get update` 
7. Run `dos2unix run.sh`
### Building Docker Image
8.Open git bash terminal in the project repository and Run command 
`docker build -t fylein-app .`
in your git bash terminal
9. Run command 
`docker run -p 4040:7755 fylein-app`
10. Everytime the image is to updated, we have to rebuild the docker container and hence have to run step 4 and 5 again, instead we can create a file named `docker-compose.yml` and add content 
`version: '3'
services:
  fylein-app:
    build: .
    ports:
      - "4040:7755"
    volumes:
      - .:/src`
in it and then run `docker compose-up` which auto updates the image.


### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```
