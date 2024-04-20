# Note
You will have to do this assignment in a unix based system. If you have windows then make sure to use the `wsl` terminal as we have to use the command `bash run.sh` in this assignment


## Test coverage upto 98%
![image](https://github.com/Rajarshi12321/fyle-interview-intern-backend/assets/94736350/693656d9-ed25-4a85-92ec-83b52b0d66c7)


### Install requirements (Using virtualenv, Original documentation)


```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
#### In my case this code was throwing error, so I created the environment named env using conda:
##### If You don't have conda installed in your system, then you have to execute following code to install miniconda for this assignment. If you already have conda installed in your system then you can skip this part
```
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
After the installation is complete, you might need to close and reopen your terminal

Test the Installation:
Verify that Miniconda is installed correctly by running:
```
conda --version
```
This should display the installed Miniconda version.

Now, you have Miniconda installed on your Unix-based system, and you can use it to create and manage Python environments.


### Now making an environment with name `env` having python=3.8 using conda (Using conda to make env)
```
conda create --name env python=3.8
conda activate env
pip install -r requirements.txt
```
Make sure every module is installed properly

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

# Run by Docker compose
```
docker-compose up --build
```


# OR Build and Run with Docker:




## Build the Docker image:

```
docker build -t <your-app-name> .
```


## Run the Docker container:

```
docker run -p 7755:7755 <your-app-name>
```

Now, your Flask application should be accessible at http://localhost:7755.




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
   
