from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class DutyScheduleBase(BaseModel):
    member_id: int
    duty_date: date
    is_completed: bool = False
    completion_notes: Optional[str] = None


class DutyScheduleCreate(DutyScheduleBase):
    pass


class DutyScheduleUpdate(BaseModel):
    member_id: Optional[int] = None
    duty_date: Optional[date] = None
    is_completed: Optional[bool] = None
    completion_notes: Optional[str] = None
    completed_at: Optional[date] = None


class DutyScheduleResponse(DutyScheduleBase):
    id: int
    completed_at: Optional[date] = None

    class Config:
        from_attributes = True


class DutyScheduleListResponse(BaseModel):
    data: List[DutyScheduleResponse]
    total: int
