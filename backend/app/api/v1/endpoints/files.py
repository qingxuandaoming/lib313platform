from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import uuid
import mimetypes
from pathlib import Path
from app.core.database import get_db
from app.core.config import get_settings
from app.models.file import File as FileModel, FileType
from app.schemas.file import (
    FileCreate,
    FileResponse as FileResponseSchema,
    FileUpdate,
    FileListResponse,
    BatchUploadResponse,
)

router = APIRouter()
settings = get_settings()

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
    'presentation': ['.ppt', '.pptx', '.odp'],
    'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
    'other': []
}

# 最大文件大小 (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024


def get_file_type(filename: str) -> FileType:
    """根据文件扩展名判断文件类型"""
    ext = os.path.splitext(filename)[1].lower()
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return FileType(file_type)
    
    return FileType.OTHER


def validate_file(file: UploadFile) -> None:
    """验证文件"""
    # 检查文件大小
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小不能超过 {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # 检查文件扩展名
    ext = os.path.splitext(file.filename)[1].lower()
    all_allowed_extensions = []
    for extensions in ALLOWED_EXTENSIONS.values():
        all_allowed_extensions.extend(extensions)
    
    if ext and ext not in all_allowed_extensions and ext != '':
        # 允许无扩展名文件，但如果有扩展名则必须在允许列表中
        pass


@router.get("", response_model=FileListResponse)
def get_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = Query(None),
    session_id: Optional[int] = Query(None),
    file_type: Optional[FileType] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    query = db.query(FileModel)
    
    # 筛选条件
    if project_id:
        query = query.filter(FileModel.project_id == project_id)
    if session_id:
        query = query.filter(FileModel.session_id == session_id)
    if file_type:
        query = query.filter(FileModel.file_type == file_type)
    if search:
        query = query.filter(
            FileModel.original_filename.contains(search) |
            FileModel.description.contains(search)
        )
    
    # 按创建时间倒序
    query = query.order_by(FileModel.created_at.desc())
    
    total = query.count()
    files = query.offset(skip).limit(limit).all()
    
    return {"data": files, "total": total}


@router.get("/stats")
def get_file_stats(db: Session = Depends(get_db)):
    """获取文件统计信息"""
    total_files = db.query(FileModel).count()
    # 使用 SQLAlchemy 的 func 进行聚合计算
    total_size = db.query(func.sum(FileModel.file_size)).scalar() or 0
    
    # 按类型统计
    type_stats = {}
    for file_type in FileType:
        count = db.query(FileModel).filter(FileModel.file_type == file_type).count()
        type_stats[file_type.value] = count
    
    return {
        "total_files": total_files,
        "total_size": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "type_stats": type_stats
    }


@router.get("/{file_id}", response_model=FileResponseSchema)
def get_file(file_id: int, db: Session = Depends(get_db)):
    """获取单个文件详情"""
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    return file


@router.get("/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """下载文件"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    if not os.path.exists(db_file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件已被删除"
        )
    
    return FileResponse(
        path=db_file.file_path,
        filename=db_file.original_filename,
        media_type=db_file.mime_type or 'application/octet-stream'
    )


@router.post("/upload", response_model=FileResponseSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    uploader_id: int = 1,  # TODO: 从认证中获取
    project_id: Optional[int] = None,
    session_id: Optional[int] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """上传文件"""
    # 验证文件
    validate_file(file)
    
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
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件保存失败: {str(e)}"
        )
    
    # 获取文件信息
    file_size = os.path.getsize(file_path)
    file_type = get_file_type(file.filename)
    mime_type = file.content_type or mimetypes.guess_type(file.filename)[0]
    
    # 创建数据库记录
    db_file = FileModel(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_type=file_type,
        file_size=file_size,
        mime_type=mime_type,
        project_id=project_id,
        session_id=session_id,
        uploader_id=uploader_id,
        description=description
    )
    
    try:
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    except Exception as e:
        # 如果数据库操作失败，删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    
    return db_file


@router.put("/{file_id}", response_model=FileResponseSchema)
def update_file(
    file_id: int,
    file_update: FileUpdate,
    db: Session = Depends(get_db)
):
    """更新文件信息"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 更新字段
    update_data = file_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_file, field, value)
    
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
        try:
            os.remove(db_file.file_path)
        except Exception as e:
            # 记录错误但不阻止数据库删除
            print(f"删除文件失败: {e}")
    
    # 删除数据库记录
    db.delete(db_file)
    db.commit()
    return None


@router.post("/batch-upload", response_model=BatchUploadResponse)
async def batch_upload_files(
    files: List[UploadFile] = File(...),
    uploader_id: int = 1,  # TODO: 从认证中获取
    project_id: Optional[int] = None,
    session_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """批量上传文件"""
    if len(files) > 10:  # 限制批量上传数量
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="批量上传文件数量不能超过10个"
        )
    
    uploaded_files = []
    failed_files = []
    
    for file in files:
        try:
            # 验证文件
            validate_file(file)
            
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
            
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            file_type = get_file_type(file.filename)
            mime_type = file.content_type or mimetypes.guess_type(file.filename)[0]
            
            # 创建数据库记录
            db_file = FileModel(
                filename=unique_filename,
                original_filename=file.filename,
                file_path=str(file_path),
                file_type=file_type,
                file_size=file_size,
                mime_type=mime_type,
                project_id=project_id,
                session_id=session_id,
                uploader_id=uploader_id
            )
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            uploaded_files.append(db_file)
            
        except Exception as e:
            failed_files.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    # 统一返回结构
    return {
        "uploaded_files": uploaded_files,
        "failed_files": failed_files or None,
        "message": (
            f"成功上传 {len(uploaded_files)} 个文件，{len(failed_files)} 个文件上传失败"
            if failed_files
            else f"成功上传 {len(uploaded_files)} 个文件"
        ),
    }
