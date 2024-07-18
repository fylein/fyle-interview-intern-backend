## Introduction

This project is a Flask application that uses PostgreSQL as the database. It is Dockerized using Docker and Docker Compose for easy setup and deployment.

## Prerequisites

- Docker
- Docker Compose

## Setup


### Step 1: Install Docker and Docker Compose

Follow the installation guides on the official websites to install Docker and Docker Compose:

- [Docker Installation](https://docs.docker.com/get-docker/)
- [Docker Compose Installation](https://docs.docker.com/compose/install/)

### Step 2: Build and Run the Application

1. **Build the Docker images**:

   ```
   docker-compose build
   ```

2. **Run the Docker containers:**:

   ```
   docker-compose up
   ```

### Step 3: Access the Application

The Flask application will be accessible at http://localhost:5000


## Stopping the Application


To stop and remove the Docker containers, press CTRL+C in the terminal where docker-compose up is running.

Alternatively, you can run:
```
docker-compose down
```
This will stop and remove the containers.

## Other useful Commands:

View the logs of the containers:
```
docker-compose logs
```

Run commands inside a container:
```
docker-compose exec <service_name> <command>
```

- For example, to open a shell inside the web container:

   ```
   docker-compose exec web sh
   ```

## Troubleshooting:

If you encounter any issues, ensure that Docker and Docker Compose are installed correctly and that there are no conflicting services running on the required ports.

For further assistance, refer to the official Docker documentation:

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)