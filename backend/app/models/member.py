from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class MemberRole(str, enum.Enum):
    LEADER = "leader"
    MEMBER = "member"
    ALUMNI = "alumni"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    student_id = Column(String(20), unique=True, nullable=False, index=True)
    grade = Column(Integer, nullable=False)  # 年级，如2021
    major = Column(String(100))
    role = Column(Enum(MemberRole), default=MemberRole.MEMBER)
    email = Column(String(100))
    phone = Column(String(20))
    avatar = Column(String(255))  # 头像文件路径
    bio = Column(Text)  # 个人简介
    github = Column(String(255))
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    projects = relationship("ProjectMember", back_populates="member")
    sessions = relationship("Session", back_populates="speaker")
    duty_schedules = relationship("DutySchedule", back_populates="member")
