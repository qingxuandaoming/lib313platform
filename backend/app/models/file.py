from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class FileType(str, enum.Enum):
    DOCUMENT = "document"  # 文档
    PRESENTATION = "presentation"  # PPT
    IMAGE = "image"  # 图片
    VIDEO = "video"  # 视频
    OTHER = "other"


class File(Base):
    """文件管理"""
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(Enum(FileType))
    file_size = Column(BigInteger)  # 文件大小（字节）
    mime_type = Column(String(100))

    # 关联关系（一个文件可以属于项目或分享会）
    project_id = Column(Integer, ForeignKey("projects.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))

    uploader_id = Column(Integer, ForeignKey("members.id"))
    description = Column(String(500))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    project = relationship("Project", back_populates="files")
    session = relationship("Session", back_populates="files")
    uploader = relationship("Member", foreign_keys=[uploader_id])
