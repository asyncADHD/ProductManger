# Project Setup with Docker

This project uses Docker to set up a development environment with Redis, a web server, a Celery worker, and a Celery beat scheduler. Follow the instructions below to get started.

## Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Docker Compose

This project consists of the following services:

1. **Redis**: In-memory data structure store, used by Celery for task queueing.
2. **Web**: Django web server.
3. **Celery**: Celery worker for processing asynchronous tasks.
4. **Celery Beat**: Celery beat scheduler for scheduling tasks.

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone https://user_cll@bitbucket.org/wt-techtest/wt_projectcode.git
    cd <repo-directory>
    ```
   
2. **Build and Start the Containers**

    Use Docker Compose to build and start the containers:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start the services defined in the `docker-compose.yml` file.

4. **Apply Database Migrations**

    After the containers are up, open a new terminal and apply the database migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Create a Superuser**

    Create a superuser to access the Django admin interface:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
