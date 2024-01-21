## Application 

There are 5 resources:
- Users
- Principal
- Students
- Teachers
- Assignments

5 Users (1 Principal, 2 students and 2 teachers) have already been created for you in the db fixture

- A principal can view all the teachers
- A principal can view all the assignments submitted and/or graded by teachers.
- A principal can re-grade the assignments already graded by the teacher.
- A student can create and edit a draft assignment
- A student can list all his created assignments
- A student can submit a draft assignment to a teacher
- A teacher can list all assignments submitted to him
- A teacher can grade an assignment submitted to him

## Challenge

Please fork the repository into your account and continue the development in your fork.

Your tasks
- Add missing APIs mentioned here and get the automated tests to pass

  1. GET /principal/assignments

     This API provides assignments that are submitted.
     Result of triggered API : https://drive.google.com/file/d/189fvawo8JwW1Spj3a5uAQU_jjb2FERyN/view?usp=sharing

  2. GET /principal/teachers

     This API provides list of teachers.
     Result of triggered API : https://drive.google.com/file/d/1OoxzVvY1Xx86kYoSVpUeymotteUnM3Ex/view?usp=sharing

  3. POST /principal/assignments/grade

     This API provides list of teachers.
     Result of triggered API : https://drive.google.com/file/d/1i41M4wWHBkQzj4D32OlCR0gNKJBnXEP-/view?usp=sharing

- Add tests for grading API

  https://drive.google.com/file/d/1r_O6aTxwt1ktGjfnxgHV6rI1q60Su-Rb/view?usp=sharing

- Please be aware that intentional bugs have been incorporated into the application, leading to test failures. Kindly address and rectify these issues as part of the assignment.

  1. bug : while running APIs, providing different user_id for different users were triggering the APIs.
     for example: X-Principal - {user_id : 1, principal_id = 1} was triggering the APIs by principal.
     fix : Added additional validations to check user authenticity in core/apis/decorators.py file

  2. bug : even after submitting assignment, the state of assignmnet was not getting updated.
     fix : Added `assignment.state = AssignmentStateEnum.SUBMITTED` in core/models/assignment.py line 72.

- All tests should pass

  Done

- Get the test coverage to 94% or above

  Added 6 more tes cases to achieve coverage above 94 %.
  Current coverage : 97%.
  Result : https://drive.google.com/file/d/1mSnYxQdXlUreXXifu8-7xpnCiL_1meOm/view?usp=sharing

- There are certain SQL tests present inside `tests/SQL/`. You have to write SQL in following files:
  - count_grade_A_assignments_by_teacher_with_max_grading.sql
    done
  - number_of_assignments_per_state.sql
    done
- Optionally, Dockerize your application by creating a Dockerfile and a docker-compose.yml file, providing clear documentation on building and running the application with Docker, to stand out in your submission

***Once you are done with your task, please use [this form](https://forms.gle/dJLNMyBmBCJSv6EH7) to complete your submission.***

You will hear back within 48 hours from us via email. 


## Available APIs

### Auth
- header: "X-Principal"
- value: {"user_id":1, "student_id":1}

For APIs to work you need a principal header to establish identity and context

### GET /student/assignments

List all assignments created by a student
```
headers:
X-Principal: {"user_id":1, "student_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T02:53:45.028101",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T02:53:45.034289"
        },
        {
            "content": "THESIS T1",
            "created_at": "2021-09-17T02:53:45.028876",
            "grade": null,
            "id": 2,
            "state": "DRAFT",
            "student_id": 1,
            "teacher_id": null,
            "updated_at": "2021-09-17T02:53:45.028882"
        }
    ]
}
```

### POST /student/assignments

Create an assignment
```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "content": "some text"
}

response:
{
    "data": {
        "content": "some text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:14:08.572560"
    }
}
```

### POST /student/assignments

Edit an assignment
```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "id": 5,
    "content": "some updated text"
}

response:
{
    "data": {
        "content": "some updated text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:15:06.349337"
    }
}
```

### POST /student/assignments/submit

Submit an assignment
```
headers:
X-Principal: {"user_id":1, "student_id":1}

payload:
{
    "id": 2,
    "teacher_id": 2
}

response:
{
    "data": {
        "content": "THESIS T1",
        "created_at": "2021-09-17T03:14:01.580467",
        "grade": null,
        "id": 2,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 2,
        "updated_at": "2021-09-17T03:17:20.147349"
    }
}

```
### GET /teacher/assignments

List all assignments submitted to this teacher
```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### POST /teacher/assignments/grade

Grade an assignment
```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```

## Missing APIs

You'll need to implement these APIs

### GET /principal/assignments

List all submitted and graded assignments
```
headers:
X-Principal: {"user_id":5, "principal_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### GET /principal/teachers

List all the teachers
```
headers:
X-Principal: {"user_id":5, "principal_id":1}


response:
{
    "data": [
        {
            "created_at": "2024-01-08T07:58:53.131970",
            "id": 1,
            "updated_at": "2024-01-08T07:58:53.131972",
            "user_id": 3
        }
    ]
}
```

### POST /principal/assignments/grade

Grade or re-grade an assignment
```
headers:
X-Principal: {"user_id":5, "principal_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```
