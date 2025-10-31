from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.member import Member
from app.models.project import Project
from app.models.session import Session as SessionModel
from app.models.device import Device
from app.models.file import File


router = APIRouter()


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    """返回系统数据统计"""
    return {
        "members": db.query(Member).count(),
        "projects": db.query(Project).count(),
        "sessions": db.query(SessionModel).count(),
        "devices": db.query(Device).count(),
        "files": db.query(File).count(),
    }