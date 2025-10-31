from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.models.duty import DutySchedule
from app.schemas.duty import DutyScheduleCreate, DutyScheduleUpdate, DutyScheduleResponse

router = APIRouter()


@router.get("", response_model=List[DutyScheduleResponse])
def get_duty_schedules(
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """获取值日安排列表"""
    query = db.query(DutySchedule)
    if start_date:
        query = query.filter(DutySchedule.duty_date >= start_date)
    if end_date:
        query = query.filter(DutySchedule.duty_date <= end_date)

    schedules = query.order_by(DutySchedule.duty_date).offset(skip).limit(limit).all()
    return schedules


@router.get("/{schedule_id}", response_model=DutyScheduleResponse)
def get_duty_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """获取单个值日安排详情"""
    schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )
    return schedule


@router.post("", response_model=DutyScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_duty_schedule(schedule: DutyScheduleCreate, db: Session = Depends(get_db)):
    """创建新值日安排"""
    # 检查该日期是否已有安排
    existing = db.query(DutySchedule).filter(
        DutySchedule.duty_date == schedule.duty_date,
        DutySchedule.member_id == schedule.member_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该成员在此日期已有值日安排"
        )

    db_schedule = DutySchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.put("/{schedule_id}", response_model=DutyScheduleResponse)
def update_duty_schedule(
    schedule_id: int,
    schedule: DutyScheduleUpdate,
    db: Session = Depends(get_db)
):
    """更新值日安排"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )

    for key, value in schedule.model_dump(exclude_unset=True).items():
        setattr(db_schedule, key, value)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.patch("/{schedule_id}/complete", response_model=DutyScheduleResponse)
def complete_duty(
    schedule_id: int,
    completion_notes: str = None,
    db: Session = Depends(get_db)
):
    """标记值日完成"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="值日安排不存在")

    db_schedule.is_completed = True
    db_schedule.completed_at = date.today()
    if completion_notes:
        db_schedule.completion_notes = completion_notes

    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_duty_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """删除值日安排"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )

    db.delete(db_schedule)
    db.commit()
    return None
