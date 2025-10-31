from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.core.database import get_db
from app.models.member import Member, MemberRole
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberListResponse, MemberStats

router = APIRouter()


@router.get("", response_model=MemberListResponse)
def get_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    role: Optional[MemberRole] = Query(None),
    grade: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """获取成员列表（标准化返回：{ data, total }）"""
    query = db.query(Member)

    # 筛选条件
    if role:
        query = query.filter(Member.role == role)
    if grade:
        query = query.filter(Member.grade == grade)
    if search:
        query = query.filter(
            Member.name.contains(search) |
            Member.major.contains(search) |
            Member.student_id.contains(search)
        )

    # 按创建时间倒序
    query = query.order_by(Member.created_at.desc())

    total = query.count()
    members = query.offset(skip).limit(limit).all()
    return {"data": members, "total": total}


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """获取单个成员详情"""
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )
    return member


@router.get("/stats", response_model=MemberStats)
def get_member_stats(db: Session = Depends(get_db)):
    """获取成员统计信息"""
    total_members = db.query(Member).count()

    # 按角色统计
    role_stats = {}
    for role in MemberRole:
        count = db.query(Member).filter(Member.role == role).count()
        role_stats[role.value] = count

    # 按年级统计
    grade_counts = db.query(Member.grade, func.count(Member.id)).group_by(Member.grade).all()
    grade_stats = {grade: count for grade, count in grade_counts}

    return {
        "total_members": total_members,
        "role_stats": role_stats,
        "grade_stats": grade_stats,
    }


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    """创建新成员"""
    # 检查学号是否已存在
    existing = db.query(Member).filter(Member.student_id == member.student_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="学号已存在"
        )

    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    member: MemberUpdate,
    db: Session = Depends(get_db)
):
    """更新成员信息"""
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )

    # 更新字段
    for key, value in member.model_dump(exclude_unset=True).items():
        setattr(db_member, key, value)

    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """删除成员"""
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )

    db.delete(db_member)
    db.commit()
    return None
