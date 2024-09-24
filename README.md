# Assignment-task-overview
This project is a RESTful API for managing assignments and grading for students and teachers

# Accomplishments:
- Passed all 18 unit tests.
- Added new tests, achieving 93% test coverage.
- The application is Dockerized.


# To run the FastAPI app using Docker

1. **Pull the Docker image:**

    ```bash
    docker pull chisty17/fyle:fastapi-app
    ```

2. **Run the Docker container:**

    ```bash
    docker run -d -p 7755:7755 chisty17/fyle:fastapi-app
    ```

  

3. **Verify the container is running (optional):**

    ```bash
    docker ps
    ```

4. **Access the application:**

    - Open your browser and go to `http://localhost:7755`.
    - Or use an API client to test the FastAPI endpoints.



