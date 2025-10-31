from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Project, Member, Session as SessionModel, Device
from app.schemas.stats import StatsResponse

router = APIRouter()


@router.get("", response_model=StatsResponse, summary="获取首页统计")
def get_stats(db: Session = Depends(get_db)):
    projects = db.query(Project).count()
    members = db.query(Member).count()
    sessions = db.query(SessionModel).count()
    devices = db.query(Device).count()

    return {
        "projects": projects,
        "members": members,
        "sessions": sessions,
        "devices": devices,
    }