
import random
import time
from datetime import datetime, timezone

import httpx

BASE_URL = "http://127.0.0.1:8000"

VEHICLES = [
    {"vehicle_id": "V101", "model": "Demo Sedan"},
    {"vehicle_id": "V102", "model": "Demo SUV"},
    {"vehicle_id": "V103", "model": "Demo Van"},
]


def register_vehicles(client):
    for vehicle in VEHICLES:
        response = client.post(
            f"{BASE_URL}/vehicles",
            json=vehicle,
        )

        if response.status_code not in (201, 409):
            response.raise_for_status()

        print(f"Vehicle ready: {vehicle['vehicle_id']}")


def generate_reading(vehicle_id):
    if random.random() < 0.10:
        temperature = random.uniform(121, 135)
    else:
        temperature = random.uniform(75, 105)

    return {
        "vehicle_id": vehicle_id,
        "speed": round(random.uniform(0, 120), 2),
        "engine_temperature": round(temperature, 2),
        "fuel_level": round(random.uniform(10, 100), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    with httpx.Client(timeout=10) as client:
        register_vehicles(client)

        print("Sending readings. Press Ctrl+C to stop.")

        try:
            while True:
                for vehicle in VEHICLES:
                    payload = generate_reading(
                        vehicle["vehicle_id"]
                    )

                    response = client.post(
                        f"{BASE_URL}/telemetry",
                        json=payload,
                    )
                    response.raise_for_status()

                    print(response.json())

                time.sleep(5)

        except KeyboardInterrupt:
            print("Simulator stopped.")


if __name__ == "__main__":
    main()
