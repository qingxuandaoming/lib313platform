from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse

router = APIRouter()


@router.get("", response_model=List[DeviceResponse])
def get_devices(
    skip: int = 0,
    limit: int = 100,
    device_type: str = None,
    db: Session = Depends(get_db)
):
    """获取设备列表"""
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    devices = query.offset(skip).limit(limit).all()
    return devices


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """获取单个设备详情"""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="设备不存在"
        )
    return device


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """创建新设备"""
    # 检查序列号是否已存在
    if device.serial_number:
        existing = db.query(Device).filter(
            Device.serial_number == device.serial_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="序列号已存在"
            )

    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """更新设备信息"""
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="设备不存在"
        )

    for key, value in device.model_dump(exclude_unset=True).items():
        setattr(db_device, key, value)

    db.commit()
    db.refresh(db_device)
    return db_device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """删除设备"""
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="设备不存在"
        )

    db.delete(db_device)
    db.commit()
    return None
