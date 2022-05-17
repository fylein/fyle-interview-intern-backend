# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to work / intern at Fyle and work with our engineering teams.

If it is for internship, you should be able to commit to at least 3 months.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

This is a web application designed in a context of a single classroom. 
Described [here](./Application.md)

### Your tasks 
1. Add missing APIs mentioned [here](./Application.md#Missing-APIs) and get the automated tests to pass 
2. Add a test for grading API
3. All tests should pass
4. Get the test coverage to 94% or above

## Submission

Once you are done with your task, please use [this form](https://forms.gle/fZex7LDo6kj1Syg7A) to complete your submission.

## What happens next?

You will hear back within 48 hours from us via email. We may request for some changes based on reviewing your code.

Subsequently, we will schedule a phone interview with a Fyle Engineer.

If that goes well, we'll make an offer. 

---

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
