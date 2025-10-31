from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.file import FileType


class FileBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_type: Optional[FileType] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    description: Optional[str] = None


class FileCreate(FileBase):
    project_id: Optional[int] = None
    session_id: Optional[int] = None
    uploader_id: int


class FileResponse(FileBase):
    id: int
    project_id: Optional[int] = None
    session_id: Optional[int] = None
    uploader_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
