from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict
from datetime import datetime
from app.models.project import ProjectStatus


class ProjectMemberBase(BaseModel):
    member_id: int
    role: Optional[str] = None


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    leader_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    tags: Optional[str] = None

    @field_validator("tags", mode="before")
    def normalize_tags(cls, v):
        # Accept list and convert to comma-separated string; pass through str/None
        if isinstance(v, list):
            return ",".join(str(x) for x in v)
        return v


class ProjectCreate(ProjectBase):
    member_ids: Optional[List[int]] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    leader_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    cover_image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    data: List[ProjectResponse]
    total: int


class ProjectStats(BaseModel):
    total_projects: int
    status_stats: Dict[str, int]
