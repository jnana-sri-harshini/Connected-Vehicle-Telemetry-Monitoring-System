# Connected Vehicle Telemetry Monitoring System

## Overview
A Python-based application that collects simulated vehicle telemetry, stores readings in a relational database, and generates alerts when configured thresholds are exceeded.

## Features
- Vehicle registration and management
- REST API for submitting and retrieving telemetry
- SQL-backed persistence using SQLite and SQLAlchemy
- Input validation using Pydantic
- Rule-based high-temperature alert generation
- Automated API tests using Pytest
- Interactive API documentation using FastAPI

## Tech Stack
Python, FastAPI, SQLite, SQLAlchemy, Pydantic, Pytest, HTTPX

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the API:

   `python -m uvicorn app.main:app --reload`

5. Open `http://127.0.0.1:8000/docs`.

## Run Tests

`python -m pytest -v`

## Run the Simulator

Start the API first, then run:

`python simulator.py`

## API Endpoints
- `GET /health`
- `GET /vehicles`
- `POST /vehicles`
- `POST /telemetry`
- `GET /vehicles/{vehicle_id}/telemetry`
- `GET /alerts`

## Limitations
This is a local prototype using simulated vehicle data. It is not a production vehicle-monitoring system.

## Future Improvements
Cloud deployment, authentication, improved monitoring, duplicate-event handling, and event-driven processing.