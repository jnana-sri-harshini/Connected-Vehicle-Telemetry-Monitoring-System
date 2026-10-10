
import logging

from sqlalchemy.orm import Session

from app.models import Telemetry, Alert

logger = logging.getLogger(__name__)

# Illustrative threshold for this project only.
ENGINE_TEMP_LIMIT = 120.0


def process_telemetry(
    db: Session,
    data: dict,
) -> Telemetry:
    try:
        reading = Telemetry(**data)
        db.add(reading)
        db.flush()

        logger.info(
            "Processing telemetry for vehicle %s",
            reading.vehicle_id,
        )

        if reading.engine_temperature > ENGINE_TEMP_LIMIT:
            alert = Alert(
                vehicle_id=reading.vehicle_id,
                telemetry_id=reading.id,
                alert_type="HIGH_ENGINE_TEMPERATURE",
                message=(
                    "Engine temperature exceeded the "
                    f"configured threshold: "
                    f"{reading.engine_temperature} C"
                ),
            )

            db.add(alert)

            logger.warning(
                "High engine temperature for vehicle %s",
                reading.vehicle_id,
            )

        db.commit()
        db.refresh(reading)

        return reading

    except Exception:
        logger.exception(
            "Failed to process telemetry for vehicle %s",
            data.get("vehicle_id"),
        )
        db.rollback()
        raise
