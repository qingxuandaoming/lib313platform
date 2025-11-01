from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionListResponse
from app.models.file import File as FileModel
import os

router = APIRouter()


@router.get("", response_model=SessionListResponse)
def get_sessions(
    skip: int = 0,
    limit: int = 100,
    semester: str = None,
    db: Session = Depends(get_db)
):
    """获取分享会列表（标准化返回：{ data, total }）"""
    query = db.query(SessionModel)
    if semester:
        query = query.filter(SessionModel.semester == semester)
    total = query.count()
    sessions = query.offset(skip).limit(limit).all()
    return {"data": sessions, "total": total}


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """获取单个分享会详情"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分享会不存在"
        )
    return session


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    """创建新分享会"""
    db_session = SessionModel(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.put("/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int,
    session: SessionUpdate,
    db: Session = Depends(get_db)
):
    """更新分享会信息"""
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分享会不存在"
        )

    for key, value in session.model_dump(exclude_unset=True).items():
        setattr(db_session, key, value)

    db.commit()
    db.refresh(db_session)
    return db_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """删除分享会"""
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分享会不存在"
        )
    # 级联删除：删除关联文件（包含物理文件）
    files = db.query(FileModel).filter(FileModel.session_id == session_id).all()
    for f in files:
        if f.file_path and os.path.exists(f.file_path):
            try:
                os.remove(f.file_path)
            except Exception as e:
                print(f"删除文件失败: {e}")
        db.delete(f)

    # 删除分享会
    db.delete(db_session)
    db.commit()
    return None
