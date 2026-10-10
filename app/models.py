
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    model: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey("vehicles.vehicle_id"),
        index=True,
    )

    speed: Mapped[float] = mapped_column(Float)

    engine_temperature: Mapped[float] = mapped_column(Float)

    fuel_level: Mapped[float] = mapped_column(Float)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        index=True,
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey("vehicles.vehicle_id"),
        index=True,
    )

    telemetry_id: Mapped[int] = mapped_column(
        ForeignKey("telemetry.id"),
    )

    alert_type: Mapped[str] = mapped_column(String(50))

    message: Mapped[str] = mapped_column(String(250))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )


Index(
    "ix_telemetry_vehicle_time",
    Telemetry.vehicle_id,
    Telemetry.timestamp,
)
