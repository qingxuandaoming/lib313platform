from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Member, Project, Session as SessionModel, Device, File


router = APIRouter()


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    members_count = db.query(Member).count()
    projects_count = db.query(Project).count()
    sessions_count = db.query(SessionModel).count()
    devices_count = db.query(Device).count()
    files_count = db.query(File).count()

    return {
        "members": members_count,
        "projects": projects_count,
        "sessions": sessions_count,
        "devices": devices_count,
        "files": files_count,
    }