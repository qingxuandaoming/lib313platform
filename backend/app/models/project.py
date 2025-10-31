from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    leader_id = Column(Integer, ForeignKey("members.id"))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    github_url = Column(String(255))
    demo_url = Column(String(255))
    tags = Column(String(255))  # 标签，逗号分隔
    cover_image = Column(String(255))  # 项目封面
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    members = relationship("ProjectMember", back_populates="project")
    files = relationship("File", back_populates="project")


class ProjectMember(Base):
    """项目成员关联表"""
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    role = Column(String(50))  # 在项目中的角色
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    project = relationship("Project", back_populates="members")
    member = relationship("Member", back_populates="projects")
