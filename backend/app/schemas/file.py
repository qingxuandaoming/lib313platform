from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.file import FileType


class FileBase(BaseModel):
    original_filename: str
    description: Optional[str] = None


class FileCreate(FileBase):
    filename: str
    file_path: str
    file_type: Optional[FileType] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    project_id: Optional[int] = None
    session_id: Optional[int] = None
    uploader_id: int


class FileUpdate(BaseModel):
    original_filename: Optional[str] = None
    description: Optional[str] = None


class FileResponse(FileBase):
    id: int
    filename: str
    file_path: str
    file_type: Optional[FileType] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    project_id: Optional[int] = None
    session_id: Optional[int] = None
    uploader_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FileStats(BaseModel):
    total_files: int
    total_size: int
    total_size_mb: float
    type_stats: dict

class FailedFileItem(BaseModel):
    filename: str
    error: str


class BatchUploadResponse(BaseModel):
    uploaded_files: List[FileResponse]
    failed_files: Optional[List[FailedFileItem]] = None
    message: Optional[str] = None


class FileListResponse(BaseModel):
    data: List[FileResponse]
    total: int
