from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import Base, engine, SessionLocal
# 导入所有模型以确保表被创建
from app.models import *

settings = get_settings()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化默认管理员
try:
    from app.services.user_service import ensure_default_admin
    db = SessionLocal()
    ensure_default_admin(db)
    db.close()
except Exception:
    # 启动时初始化失败不阻塞服务
    pass

app = FastAPI(
    title="313实验室开放平台 API",
    description="实验室成员、项目、分享会、设备管理平台",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "欢迎使用313实验室开放平台API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 注册路由
from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
