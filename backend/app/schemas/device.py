from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.device import DeviceStatus


class DeviceBase(BaseModel):
    name: str
    device_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    specifications: Optional[str] = None
    status: DeviceStatus = DeviceStatus.AVAILABLE
    location: Optional[str] = None
    current_user_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    specifications: Optional[str] = None
    status: Optional[DeviceStatus] = None
    location: Optional[str] = None
    current_user_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
