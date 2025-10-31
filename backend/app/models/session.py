from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Session(Base):
    """分享会"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_number = Column(Integer, nullable=False)  # 第几期
    semester = Column(String(20), nullable=False)  # 学期，如"2024-1"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    speaker_id = Column(Integer, ForeignKey("members.id"))
    session_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(100))
    cover_image = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    speaker = relationship("Member", back_populates="sessions")
    files = relationship("File", back_populates="session")
