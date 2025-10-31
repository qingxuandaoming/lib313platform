from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.member import MemberRole


class MemberBase(BaseModel):
    name: str
    student_id: str
    grade: int
    major: Optional[str] = None
    role: MemberRole = MemberRole.MEMBER
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[int] = None
    major: Optional[str] = None
    role: Optional[MemberRole] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    github: Optional[str] = None
    avatar: Optional[str] = None


class MemberResponse(MemberBase):
    id: int
    avatar: Optional[str] = None
    joined_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemberListResponse(BaseModel):
    data: List[MemberResponse]
    total: int
