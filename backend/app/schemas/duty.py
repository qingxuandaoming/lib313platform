from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.schemas.member import MemberResponse


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
    member: Optional[MemberResponse] = None

    class Config:
        from_attributes = True


class DutyScheduleListResponse(BaseModel):
    data: List[DutyScheduleResponse]
    total: int


class DutyGenerateRequest(BaseModel):
    start_date: date
    weeks: int = 1
    prefer_same_grade: bool = True
    skip_weekends: bool = False

    class Config:
        from_attributes = True
