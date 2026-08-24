# Smart Hotel Reservation System – AI Powered

## Overview

Smart Hotel Reservation System is a FastAPI-based hotel booking application with:

- PostgreSQL-backed booking persistence
- Alembic database migrations
- Machine learning-based booking scoring
- OCR-based identity data extraction
- Google Cloud Storage integration for uploaded identity images
- Email booking agent support
- Docker and Docker Compose deployment
- Reproducible Python dependencies
- Automated linting, testing, coverage, dependency, and Docker validation in CI

## Project Requirements

The supported development environment uses:

- Python 3.12
- Docker and Docker Compose for containerized execution
- PostgreSQL when running the application locally or with Compose

## Fresh Clone Setup

Clone the repository and enter the project directory:

~~~bash
git clone <repository-url>
cd Smart-Hotel-Reservation-System-AI-Powered
~~~

Create and activate a virtual environment:

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
~~~

Install the locked dependencies:

~~~bash
python -m pip install --upgrade pip
python -m pip install pip-tools==7.6.1
python -m piptools sync requirements.txt requirements-dev.txt
~~~

Verify the installed environment:

~~~bash
python -m pip check
~~~

## Dependency Management

Runtime dependencies are declared in:

- `requirements.in`

Development dependencies are declared in:

- `requirements-dev.in`

The locked dependency files are:

- `requirements.txt`
- `requirements-dev.txt`

To regenerate the lock files:

~~~bash
python -m piptools compile requirements.in
python -m piptools compile requirements-dev.in
~~~

To verify that the dependency declarations are reproducible without modifying the lock files:

~~~bash
python -m piptools compile --dry-run requirements.in
python -m piptools compile --dry-run requirements-dev.in
~~~

## Environment Configuration

Create the local environment file:

~~~bash
cp .env.example .env
~~~

Review `.env.example` and provide appropriate values for your local environment.

The application database configuration is controlled through environment variables.

## Database Setup

The project uses Alembic for schema migrations.

Configure the database environment variables, then run:

~~~bash
alembic upgrade head
~~~

To verify the current migration state:

~~~bash
alembic current
~~~

To generate SQL without connecting to the database:

~~~bash
alembic upgrade head --sql
~~~

## Running the Application Locally

From the project root:

~~~bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
~~~

The API will be available at:

~~~text
http://localhost:8000
~~~

Interactive API documentation:

~~~text
http://localhost:8000/docs
~~~

## Running Tests

Run the complete backend test suite:

~~~bash
pytest backend/tests -q
~~~

Run the service tests only:

~~~bash
pytest backend/tests/test_ocr_service.py \
       backend/tests/test_gcs_service.py \
       -q
~~~

Run the API tests:

~~~bash
pytest backend/tests/test_booking_api.py -q
~~~

## Linting

Run Ruff across the backend and Alembic configuration:

~~~bash
ruff check backend alembic
~~~

Apply supported automatic fixes:

~~~bash
ruff check backend alembic --fix
~~~

## Coverage

The CI coverage command can also be run locally:

~~~bash
pytest backend/tests \
  --cov=app \
  --cov=agents \
  --cov=services \
  --cov=ml \
  --cov-report=term-missing \
  --cov-fail-under=85 \
  -q
~~~

## Docker Compose

Validate the Docker Compose configuration:

~~~bash
docker compose --env-file .env.example config --quiet
~~~

Build and start the services:

~~~bash
docker compose --env-file .env.example up --build
~~~

Run the services in detached mode:

~~~bash
docker compose --env-file .env.example up --build -d
~~~

Stop the services:

~~~bash
docker compose down
~~~

The API service waits for the PostgreSQL health check before starting.

## Docker API Image

Build the API image:

~~~bash
docker compose --env-file .env.example build api
~~~

Start only the API service and its dependencies:

~~~bash
docker compose --env-file .env.example up api
~~~

The API container runs Alembic migrations before starting Uvicorn.

## CI

GitHub Actions validates:

- Dependency installation using the locked dependency files
- Dependency consistency with `pip check`
- Reproducibility of dependency declarations
- Ruff linting
- Backend tests
- Coverage requirements
- Docker Compose configuration
- API Docker image builds
- Basic repository secret detection
- Generated artifact hygiene

## Project Structure

~~~text
.
├── alembic/
│   ├── env.py
│   └── versions/
├── backend/
│   ├── agents/
│   │   └── email_agent.py
│   ├── app/
│   │   ├── api.py
│   │   ├── database.py
│   │   ├── inference.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── database/
│   │   └── legacy_hotel_bookings.sql
│   ├── ml/
│   ├── services/
│   │   ├── gcs.py
│   │   └── ocr.py
│   └── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic.ini
├── Dockerfile.api
├── docker-compose.yml
├── requirements.in
├── requirements.txt
├── requirements-dev.in
└── requirements-dev.txt
~~~

## Repository Hygiene

Do not commit:

- `.env` files containing credentials
- Local database files
- Generated coverage artifacts
- Local machine-learning model artifacts
- Private keys or cloud credentials

Use `.env.example` as the template for required configuration.

## Verification Checklist

For a fresh clone, the following commands should complete successfully after dependency installation and environment configuration:

~~~bash
python -m pip check
ruff check backend alembic
pytest backend/tests -q
pytest backend/tests \
  --cov=app \
  --cov=agents \
  --cov=services \
  --cov=ml \
  --cov-report=term-missing \
  --cov-fail-under=85 \
  -q
docker compose --env-file .env.example config --quiet
docker compose --env-file .env.example build api
~~~
