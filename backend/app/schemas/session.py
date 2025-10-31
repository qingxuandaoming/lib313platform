from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SessionBase(BaseModel):
    session_number: int
    semester: str
    title: str
    description: Optional[str] = None
    speaker_id: int
    session_date: datetime
    location: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    session_number: Optional[int] = None
    semester: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    speaker_id: Optional[int] = None
    session_date: Optional[datetime] = None
    location: Optional[str] = None
    cover_image: Optional[str] = None


class SessionResponse(SessionBase):
    id: int
    cover_image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    data: List[SessionResponse]
    total: int
