
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError

from app.database import Base, engine, get_db
from app.models import Vehicle, Telemetry, Alert
from app.schemas import (
    VehicleCreate,
    VehicleResponse,
    TelemetryCreate,
    TelemetryResponse,
)
from app.services import process_telemetry

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Connected Vehicle Telemetry Monitoring System",
    description="API for vehicle readings and alerts",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/vehicles",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
):
    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)

    try:
        db.commit()
        db.refresh(vehicle)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Vehicle already exists",
        )

    return vehicle


@app.get("/vehicles", response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db)):
    return db.scalars(
        select(Vehicle).order_by(Vehicle.id)
    ).all()


@app.post(
    "/telemetry",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_telemetry(
    data: TelemetryCreate,
    db: Session = Depends(get_db),
):
    vehicle = db.scalar(
        select(Vehicle).where(
            Vehicle.vehicle_id == data.vehicle_id
        )
    )

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found. Register it first.",
        )

    values = data.model_dump(exclude={"timestamp"})

    if data.timestamp is not None:
        values["timestamp"] = data.timestamp

    return process_telemetry(db, values)


@app.get("/vehicles/{vehicle_id}/telemetry")
def get_vehicle_telemetry(
    vehicle_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    vehicle = db.scalar(
        select(Vehicle).where(
            Vehicle.vehicle_id == vehicle_id
        )
    )

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    limit = max(1, min(limit, 200))

    query = (
        select(Telemetry)
        .where(Telemetry.vehicle_id == vehicle_id)
        .order_by(
            desc(Telemetry.timestamp),
            desc(Telemetry.id),
        )
        .limit(limit)
    )

    return db.scalars(query).all()


@app.get("/alerts")
def list_alerts(
    vehicle_id: str | None = None,
    db: Session = Depends(get_db),
):
    query = select(Alert).order_by(
        desc(Alert.created_at),
        desc(Alert.id),
    )

    if vehicle_id is not None:
        query = query.where(Alert.vehicle_id == vehicle_id)

    return db.scalars(query.limit(200)).all()
