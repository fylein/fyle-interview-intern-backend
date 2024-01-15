# Project Documentation


## Cloning the Repository

1. Open a terminal on your local machine.

2. Run the following command to clone the repository:

    ```bash
        git clone https://github.com/Hrishabh17/fyle-interview-intern-backend.git
    ```

3. Change into the project directory:

    ```bash
    cd dir_name
    ```

    Replace `dir_name` with the name of the directory where the repository is cloned.



## Building and Running the Docker Container

1. Ensure that you have Docker installed on your machine.

2. Build the Docker image:

    ```bash
        docker-compose build
    ```

3. Run the Docker container:

    ```bash
        docker-compose up
    ```

    If you want to run the services in the background, use the `-d` option:

    ```bash
        docker-compose up -d
    ```

4. Access the application in your browser at [http://localhost:7755].

## Missing APIs

### 1. [GET] /principal/assignments

List all submitted and graded assignments.

#### Request:

```http
GET /principal/assignments
Headers:
  X-Principal: {"user_id":5, "principal_id":1}

```
#### Response 
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


### 2. [GET] /principal/teachers

List all the teachers.

#### Request:

```http
GET /principal/teachers
Headers:
  X-Principal: {"user_id":5, "principal_id":1}

```
#### Response 
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


### 3. [POST] /principal/assignments/grade

Grade or re-grade an assignment.

#### Request:

```http
GET /principal/teachers
Headers:
  X-Principal: {"user_id":5, "principal_id":1}
Payload:
  {
      "id":  1,
      "grade": "A"
  }
```
#### Response 
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


### Testing

All tests have been successfully executed, achieving a 100% passing score.



