from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class DeviceStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Device(Base):
    """设备管理"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)  # computer, server, printer等
    brand = Column(String(50))
    model = Column(String(100))
    serial_number = Column(String(100), unique=True)
    specifications = Column(Text)  # 配置信息，JSON格式
    status = Column(Enum(DeviceStatus), default=DeviceStatus.AVAILABLE)
    location = Column(String(100))
    current_user_id = Column(Integer, ForeignKey("members.id"))
    purchase_date = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    current_user = relationship("Member", foreign_keys=[current_user_id])
