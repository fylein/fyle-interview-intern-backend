# Classroom Service API

## Project Overview
This is a Flask-based API for managing classroom interactions between Principals, Teachers, and Students. The application allows students to submit assignments, teachers to grade them, and principals to review all activities.

## API Endpoints
- **POST** `/login` – Authenticate and get JWT token.
- **GET** `/principal/assignments` – List all assignments.
- **PUT** `/principal/assignments/<assignment_id>/regrade` – Regrade an assignment.
- **GET** `/teacher/assignments` – List assignments graded by a teacher.
- **POST** `/student/assignments` – Submit a new assignment.

## Test Coverage
Test coverage was achieved using `pytest` with over 94% coverage across the project.