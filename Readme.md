# Flask Application with Docker

This is a simple Flask application Dockerized for easy deployment.

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose (optional): [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to build and run the Flask application with Docker:

1. Clone the repository:

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```


2. Build the Docker image:
    
    ```
    docker build -t <my-flask-app> .
    ```
    Replace <my-flask-app> with the desired name for your Docker image.

3. Run the Docker container:
    
    ```
    docker run -d -p 7755:7755 my-flask-app
    ```
    This command starts the container in detached mode and maps port 7755 of the host to port 7755 of the container.

4. Access your Flask application:

    Once the container is running, you can access your Flask application by opening a web browser and navigating to http://localhost:7755 or http://<host-ip>:7755 if you're using a remote server.


# Using Docker Compose

If you prefer to use Docker Compose for managing your application, follow these steps:

1. Build and run the Docker container using Docker Compose:

    ```
    docker-compose up -d
    ```

2. Once the container is running, you can access your Flask application by opening a web browser and navigating to http://localhost:7755 or http://<host-ip>:7755 if you're using a remote server.

