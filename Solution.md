# Solution Fyle Interview Intern Backend Application 

## Introduction
At every change in the code in following format a comment is added at the start
```
# Change : .....
```

## Main Additions

### 0. Data Base for testing
1. One of the main issue is original database (store.sqliyte3) state is changing after pytesting.
2. I tried to solve it by

    -   create a copy of original database at start of test initialization(copy_db.sqlite3).
    -   after pytesting, I copied the copy_db.sqlite3 database to original database (store.sqliyte3)


### 1. Missing APIs 
All the missings are added/created

### 2. Tests
1. Additional Tests are created.
2. All tests are passed.
3. Test coverage is 99%.

**Note :** In ,core/server.py, statements at line 43 and 51 are not getting testing. Both errors 1. integrity error, 2. Internal Error. Based on the APIs and remaining additions, "I think we won't be able to get integrity and internal error." If we ignore both conditions in server.py we will get 100% coverage of the tests.

**Note :**  Use below command for pytesting and get info about which are statements are not being tests also
```
pytest --cov --cov-report term-missing -vvv -s tests/
```

**OUTPUT**
```
---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
core/__init__.py                        20      0   100%
core/apis/__init__.py                    0      0   100%
core/apis/assignments/__init__.py        3      0   100%
core/apis/assignments/principal.py      22      0   100%
core/apis/assignments/schema.py         36      0   100%
core/apis/assignments/student.py        33      0   100%
core/apis/assignments/teacher.py        22      0   100%
core/apis/decorators.py                 31      0   100%
core/apis/responses.py                   5      0   100%
core/apis/teachers/__init__.py           1      0   100%
core/apis/teachers/principal.py         13      0   100%
core/apis/teachers/schema.py            11      0   100%
core/libs/__init__.py                    0      0   100%
core/libs/assertions.py                 15      0   100%
core/libs/exceptions.py                 10      0   100%
core/libs/helpers.py                    10      0   100%
core/models/__init__.py                  0      0   100%
core/models/assignments.py              78      0   100%
core/models/students.py                 10      0   100%
core/models/teachers.py                 17      0   100%
core/server.py                          28      2    93%   43, 51
------------------------------------------------------------------
TOTAL                                  365      2    99%


================================================ 32 passed in 0.42s =================================================
```

### 3. SQL
Both SQL statements are added

### 4. Dockerize

**NOTE :** Please go to [Dockerize_Solution](Dockerize_Solution.md) for dockerization commands of the application


If you want to use docker image only
## Docker Image/Container

### 1. Dockerfile
Go to location of Dockerfile directory
```
docker build -t <image_name> .
```

### 2. Run container
Change variables based on your requirements.
```
docker run -it -p 7755:7755 --name my_container IMAGE:TAG /bin/bash
```
### 3. Use docker container
#### Now you start server
```
bash run.sh
```
#### Run tests
```
pytest --cov --cov-report term-missing -vvv -s tests/
```
