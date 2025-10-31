from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.user import User


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, full_name: Optional[str] = None, email: Optional[str] = None, role: str = "admin") -> User:
    user = User(
        username=username,
        full_name=full_name,
        email=email,
        hashed_password=get_password_hash(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_default_admin(db: Session) -> User:
    settings = get_settings()
    username = getattr(settings, "ADMIN_USERNAME", "admin")
    password = getattr(settings, "ADMIN_PASSWORD", "admin123")

    user = get_user_by_username(db, username)
    if user:
        # 确保默认管理员可用：重置密码为配置值并激活
        user.hashed_password = get_password_hash(password)
        user.is_active = True
        db.commit()
        db.refresh(user)
        return user

    return create_user(db, username=username, password=password, full_name="Administrator", role="admin")