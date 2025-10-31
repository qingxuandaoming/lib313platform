from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class DutySchedule(Base):
    """值日安排"""
    __tablename__ = "duty_schedules"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    duty_date = Column(Date, nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    completion_notes = Column(Text)  # 完成情况备注
    completed_at = Column(Date)

    # 关系
    member = relationship("Member", back_populates="duty_schedules")
