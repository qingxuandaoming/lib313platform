from fastapi import APIRouter
from app.api.v1.endpoints import members, projects, sessions, devices, duty, files

api_router = APIRouter()

api_router.include_router(members.router, prefix="/members", tags=["成员管理"])
api_router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["分享会"])
api_router.include_router(devices.router, prefix="/devices", tags=["设备管理"])
api_router.include_router(duty.router, prefix="/duty", tags=["值日管理"])
api_router.include_router(files.router, prefix="/files", tags=["文件管理"])
