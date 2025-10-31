from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from pathlib import Path
from app.core.database import get_db
from app.core.config import get_settings
from app.models.file import File as FileModel
from app.schemas.file import FileCreate, FileResponse

router = APIRouter()
settings = get_settings()


@router.get("", response_model=List[FileResponse])
def get_files(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    session_id: int = None,
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    query = db.query(FileModel)
    if project_id:
        query = query.filter(FileModel.project_id == project_id)
    if session_id:
        query = query.filter(FileModel.session_id == session_id)

    files = query.offset(skip).limit(limit).all()
    return files


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    """获取单个文件详情"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    return file


@router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    uploader_id: int = 1,
    project_id: int = None,
    session_id: int = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    """上传文件"""
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # 确定保存路径
    if project_id:
        save_dir = Path(settings.UPLOAD_DIR) / "projects" / str(project_id)
    elif session_id:
        save_dir = Path(settings.UPLOAD_DIR) / "sessions" / str(session_id)
    else:
        save_dir = Path(settings.UPLOAD_DIR) / "others"

    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / unique_filename

    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 创建数据库记录
    db_file = FileModel(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        mime_type=file.content_type,
        project_id=project_id,
        session_id=session_id,
        uploader_id=uploader_id,
        description=description
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """删除文件"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # 删除物理文件
    if os.path.exists(db_file.file_path):
        os.remove(db_file.file_path)

    # 删除数据库记录
    db.delete(db_file)
    db.commit()
    return None
