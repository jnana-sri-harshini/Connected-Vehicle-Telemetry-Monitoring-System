
# Connected Vehicle Telemetry Monitoring System

## About the Project

I built this project to explore how vehicle data can be collected, stored, and monitored using Python. The idea is to simulate a connected-car system where vehicles continuously send information such as speed, engine temperature, and fuel level.

The application stores these readings in a database and checks for unusual values. For example, when an engine temperature exceeds a configured threshold, the system generates an alert that can be retrieved through an API.

This project helped me get hands-on experience with REST API development, database management, data validation, and automated testing.

## What It Can Do

- Register vehicles and keep track of their details.
- Receive telemetry readings through a REST API.
- Store vehicle readings in a SQLite database.
- Detect high engine-temperature readings and generate alerts.
- Retrieve a vehicle's recent telemetry history.
- Validate incoming data and handle invalid requests.
- Run automated tests to check that the application behaves as expected.
- Generate sample readings for multiple vehicles using a simulator.

## Technologies Used

- **Python** – Core application logic
- **FastAPI** – Building the REST API
- **SQLite** – Storing vehicle information and telemetry
- **SQLAlchemy** – Working with the database
- **Pydantic** – Validating incoming data
- **Pytest** – Testing the application
- **HTTPX** – Sending API requests from tests and the simulator

## Getting Started

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Connected-Vehicle-Telemetry-Monitoring-System
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository's actual URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows, activate it using:

```powershell
.venv\Scripts\activate
```

### 3. Install the Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the Application

```bash
python -m uvicorn app.main:app --reload
```

Once the server starts, open the interactive API documentation:

http://127.0.0.1:8000/docs

You can use this page to register vehicles, submit telemetry readings, and view alerts.

## Available API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the application is running |
| POST | `/vehicles` | Register a vehicle |
| GET | `/vehicles` | View registered vehicles |
| POST | `/telemetry` | Submit a telemetry reading |
| GET | `/vehicles/{vehicle_id}/telemetry` | View a vehicle's readings |
| GET | `/alerts` | View generated alerts |

## Trying It Out

First, register a vehicle using `POST /vehicles`:

```json
{
  "vehicle_id": "V101",
  "model": "Demo Sedan"
}
```

Then submit a telemetry reading using `POST /telemetry`:

```json
{
  "vehicle_id": "V101",
  "speed": 60,
  "engine_temperature": 90,
  "fuel_level": 75
}
```

To see the alert system in action, submit another reading with an engine temperature of `130`. The application should generate a high-temperature alert because the configured demonstration threshold is 120°C.

You can retrieve the generated alert using `GET /alerts`.

*Note: The temperature threshold is for demonstration purposes and is not an official automotive safety limit.*

## Running the Simulator

The project includes a simulator that generates sample telemetry for multiple vehicles.

Keep the API server running, open another terminal, activate the virtual environment, and execute:

```bash
python simulator.py
```

The simulator registers the sample vehicles if needed and periodically sends new readings to the API. Press `Ctrl+C` to stop it.

## Running the Tests

To run the automated tests, execute:

```bash
python -m pytest -v
```

The tests cover basic API functionality, vehicle registration, duplicate registrations, invalid data, unknown vehicles, and alert generation.

## What I Learned

Working on this project gave me practical experience with:

- Designing REST API endpoints and handling HTTP responses.
- Organizing a Python application into separate modules.
- Storing and retrieving data using SQLAlchemy and SQLite.
- Validating user input and handling errors.
- Writing automated tests and checking application behavior.
- Simulating incoming data to test a monitoring workflow.

## Future Improvements

There are several areas I would like to explore next, including cloud deployment, authentication, better application monitoring, duplicate-event handling, and event-driven processing using a message broker such as Kafka.

## Current Limitations

This is a learning project that uses simulated vehicle data and a local SQLite database. It is not connected to real vehicles and is not intended for production use.
