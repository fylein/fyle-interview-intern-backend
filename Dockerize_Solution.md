# Dockerizing Fyle Interview Intern Backend Application (Solution Branch)

## Introduction
This guide will walk you through the process of Dockerizing the Fyle Interview Intern Backend application. The solution branch (`srihari-sirisipalli-submission`) contains the Docker configuration files and modifications needed to run the application in a Docker container.



## Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/srihari-sirisipalli/fyle-interview-intern-backend.git
cd fyle-interview-intern-backend
```

### Step 2: Switch to the Solution Branch
```bash
git checkout srihari-sirisipalli-submission
```

### Step 3: Create a Dockerfile
Make sure you have a file named `Dockerfile` in the root of your project with the following content:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /fyle-interview-intern-backend

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Set Flask app environment variable
ENV FLASK_APP=core/server.py

# Remove the SQLite database file
RUN rm core/store.sqlite3

# Perform database migrations
RUN flask db upgrade -d core/migrations/

# Expose port 7755 for the Flask development server
EXPOSE 7755
```

### Step 4: Create a Docker Compose File
Make sure you have a file named `docker-compose.yml` in the root of your project with the following content:

```yaml
version: '3'

services:
  postgres_db:
    image: postgres:latest
    environment:
      POSTGRES_DB: credit_approval_db
      POSTGRES_USER: sri
      POSTGRES_PASSWORD: 123
    ports:
      - "5432:5432"
    networks:
      - my_network

  django_app:
    build:
      context: .
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./credit_approval_system
    ports:
      - "8000:8000"
    depends_on:
      - postgres_db
    networks:
      - my_network

networks:
  my_network:
    driver: bridge
```

### Step 5: Build and Run the Docker Containers
```bash
docker-compose up --build
```

This command will build the Docker images and start the containers. The application should be accessible at http://0.0.0.0:8000.

### Step 6: Stop and Remove Containers
To stop and remove the Docker containers, use the following command:

```bash
docker-compose down
```
