# Project Overview

This project consists of two main services: **Data Provider** and **Dashboard Service**. The Data Provider service is responsible for handling booking and cancellation events, while the Dashboard Service aggregates this data for reporting purposes.

## Services

### Data Provider

- **Description**: API for booking and cancellation events.
- **Dependencies**:
  - FastAPI
  - Uvicorn
  - Tortoise ORM
  - Asyncpg
  - Celery (with Redis)
- **URL**: http://localhost:8000

- **Swagger Documentation**: Access the Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

### Dashboard Service

- **Description**: API to view hotel booking data on a monthly and daily basis.
- **Dependencies**:
  - FastAPI
  - Uvicorn
  - Tortoise ORM
  - Asyncpg
  - Celery (with Redis)
  - Requests
- **URL**: http://localhost:8001

- **Swagger Documentation**: Access the Swagger UI at [http://localhost:8001/docs](http://localhost:8001/docs)

## Running the Application

To run the entire application, including both services and the Redis broker, use the following command:
```bash
docker-compose up --build
```
If your docker is latest, you might run with `docker compose up --build` instead.
This will start all services defined in the `docker-compose.yml` file.


## Database

Both services use PostgreSQL as their database. The following environment variables are used for database configuration:

- **Data Provider**:
  - POSTGRES_DB: data_provider_db
  - POSTGRES_USER: data_provider_user
  - POSTGRES_PASSWORD: data_provider_password

- **Dashboard Service**:
  - POSTGRES_DB: dashboard_service_db
  - POSTGRES_USER: dashboard_service_user
  - POSTGRES_PASSWORD: dashboard_service_password

## Celery Tasks

The Dashboard Service includes a Celery task that periodically updates the dashboard data by fetching events from the Data Provider. The task is scheduled to run every 60 seconds.

## API Endpoints

### Data Provider API

- **POST /events**: Create a new event.
- **GET /events**: Retrieve events based on various filters.

### Dashboard Service API

- **GET /dashboard**: Retrieve dashboard data for a given hotel and period (monthly or daily).

## License

This project is licensed under the MIT License.
