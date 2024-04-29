# Fyle Application in Docker

This repository contains a Flask-based application `Fyle` that can be run in a Docker container.

## Prerequisites

- Docker installed on your system
- Make (optional, but recommended for easier management)

## Getting Started

### Using Docker Compose

1. Clone the repository:

   ```
   git clone https://github.com/jagrit007/fyle-interview-intern-backend
   cd fyle-interview-intern-backend
   ```

2. Build and start the Docker container:

   ```
   docker-compose up -d
   ```

   This will build the Docker image and start the container in detached mode.

3. Access the application:

   The application will be available at `http://localhost:7755`.

### Using Make

1. Clone the repository:

   ```
   git clone https://github.com/jagrit007/fyle-interview-intern-backend
   cd fyle-interview-intern-backend
   ```

2. Build the Docker image:

   ```
   make build
   ```

3. Start the Docker container:

   ```
   make run
   ```

   This will start the container in detached mode.

4. Access the application:

   The application will be available at `http://localhost:7755`.

## Available Make Commands

- `build`: Build the Docker image with the tag `fyle_app`.
- `run`: Start the Docker container with the name `fyle` and map port `7755` to the host.
- `stop`: Stop the running Docker container with the name `fyle`.
- `rm`: Remove the Docker container with the name `fyle`.
- `clean`: Stop and remove the Docker container with the name `fyle`.
- `purge`: Stop and remove the Docker container with the name `fyle`, and remove the `fyle_app` image.
- `update`: Stop and remove the Docker container with the name `fyle`, build a new image with the tag `fyle_app`, and start a new container.
- `logs`: Follow the logs of the Docker container with the name `fyle`.
- `production`: Start the application using Docker Compose.

## Troubleshooting

If you encounter any issues, you can check the logs of the Docker container using the `make logs` command.
