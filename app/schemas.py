
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class VehicleCreate(BaseModel):
    vehicle_id: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)


class VehicleResponse(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TelemetryCreate(BaseModel):
    vehicle_id: str = Field(min_length=1, max_length=50)
    speed: float = Field(ge=0, le=400)
    engine_temperature: float = Field(ge=-50, le=250)
    fuel_level: float = Field(ge=0, le=100)
    timestamp: datetime | None = None


class TelemetryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: str
    speed: float
    engine_temperature: float
    fuel_level: float
    timestamp: datetime
