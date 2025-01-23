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


## Installation

1. **Please ensure that you don't fork this repository. We want your submission to be private to avoid plagiarism**
2. Clone the repo to your local and ensure you push your code into your own **private repository** on GitHub.

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


## Submission

For submitting the assignment, please follow these steps:

* Ensure that you push your code into a private repository on GitHub.
* Add `KirtiGautam`, `kartikeyrajvaidya`, `sumanth-fyle1` and `satyamyesj` as collaborators to your repository with Admin access.
* For steps to add a collaborator to your repository, refer to [this link](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository).

**Once you are done with your task, please use [this form](https://forms.gle/7ZBydqaoWaJTDYCA8) to complete your submission.**

Once you submit the assignment, you will hear back from us within 48 hours from us via email. 

We look forward to seeing your solution!