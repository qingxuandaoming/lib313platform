from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict
from datetime import date, timedelta
from app.core.database import get_db
from app.models.duty import DutySchedule
from app.models.member import Member
from app.schemas.duty import (
    DutyScheduleCreate,
    DutyScheduleUpdate,
    DutyScheduleResponse,
    DutyScheduleListResponse,
    DutyGenerateRequest,
)

router = APIRouter()


@router.get("", response_model=DutyScheduleListResponse)
def get_duty_schedules(
    skip: int = 0,
    limit: int = 100,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """获取值日安排列表（标准化返回：{ data, total }）"""
    query = db.query(DutySchedule).options(joinedload(DutySchedule.member))
    if start_date:
        query = query.filter(DutySchedule.duty_date >= start_date)
    if end_date:
        query = query.filter(DutySchedule.duty_date <= end_date)

    total = query.count()
    schedules = query.order_by(DutySchedule.duty_date).offset(skip).limit(limit).all()
    return {"data": schedules, "total": total}


@router.get("/{schedule_id}", response_model=DutyScheduleResponse)
def get_duty_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """获取单个值日安排详情"""
    schedule = db.query(DutySchedule).options(joinedload(DutySchedule.member)).filter(DutySchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )
    return schedule


@router.post("", response_model=DutyScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_duty_schedule(schedule: DutyScheduleCreate, db: Session = Depends(get_db)):
    """创建新值日安排"""
    # 检查该日期是否已有安排
    existing = db.query(DutySchedule).filter(
        DutySchedule.duty_date == schedule.duty_date,
        DutySchedule.member_id == schedule.member_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该成员在此日期已有值日安排"
        )

    db_schedule = DutySchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    # 重新查询以加载关系
    db_schedule = db.query(DutySchedule).options(joinedload(DutySchedule.member)).filter(DutySchedule.id == db_schedule.id).first()
    return db_schedule


@router.put("/{schedule_id}", response_model=DutyScheduleResponse)
def update_duty_schedule(
    schedule_id: int,
    schedule: DutyScheduleUpdate,
    db: Session = Depends(get_db)
):
    """更新值日安排"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )

    for key, value in schedule.model_dump(exclude_unset=True).items():
        setattr(db_schedule, key, value)

    db.commit()
    # 重新查询以加载关系
    db_schedule = db.query(DutySchedule).options(joinedload(DutySchedule.member)).filter(DutySchedule.id == schedule_id).first()
    return db_schedule


@router.patch("/{schedule_id}/complete", response_model=DutyScheduleResponse)
def complete_duty(
    schedule_id: int,
    completion_notes: str = None,
    db: Session = Depends(get_db)
):
    """标记值日完成"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="值日安排不存在")

    db_schedule.is_completed = True
    db_schedule.completed_at = date.today()
    if completion_notes:
        db_schedule.completion_notes = completion_notes

    db.commit()
    db_schedule = db.query(DutySchedule).options(joinedload(DutySchedule.member)).filter(DutySchedule.id == schedule_id).first()
    return db_schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_duty_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """删除值日安排"""
    db_schedule = db.query(DutySchedule).filter(DutySchedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="值日安排不存在"
        )

    db.delete(db_schedule)
    db.commit()
    return None


@router.post("/generate", response_model=DutyScheduleListResponse, status_code=status.HTTP_201_CREATED)
def generate_duty_schedule(payload: DutyGenerateRequest, db: Session = Depends(get_db)):
    """按周生成值日排班

    规则：
    - 优先同一年级为一组；每周由一个年级小组负责。
    - 该周内按组内成员轮换分配每天的值日（默认 7 天）。
    - 若某天已存在任意值日安排，则跳过该天以避免重复。
    """

    # 获取全部成员并按照年级分组（同年级为一组）
    members: List[Member] = db.query(Member).order_by(Member.grade.asc(), Member.id.asc()).all()
    if not members:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="没有可用于排班的成员")

    grade_groups: Dict[int, List[Member]] = {}
    for m in members:
        grade_groups.setdefault(m.grade, []).append(m)

    grades = sorted(grade_groups.keys())
    if not grades:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到有效年级分组")

    start_date: date = payload.start_date
    weeks: int = max(1, payload.weeks or 1)
    skip_weekends: bool = bool(payload.skip_weekends)

    created: List[DutySchedule] = []
    # 每个年级的轮换起始索引，保证同组内轮换公平
    rotate_idx: Dict[int, int] = {g: 0 for g in grades}

    for w in range(weeks):
        week_start = start_date + timedelta(days=w * 7)
        # 选择该周负责的年级（按年级序列轮换）
        group_grade = grades[w % len(grades)]
        group_members = grade_groups[group_grade]

        if not group_members:
            continue

        # 一周的每天生成安排
        day_count = 7
        assign_idx_start = rotate_idx[group_grade]

        for d in range(day_count):
            duty_day = week_start + timedelta(days=d)

            if skip_weekends:
                # 0=Monday .. 6=Sunday；跳过周六(5)与周日(6)
                if duty_day.weekday() >= 5:
                    continue

            # 若该日期已有任意安排，则跳过（避免重复）
            exists = db.query(DutySchedule).filter(DutySchedule.duty_date == duty_day).first()
            if exists:
                continue

            # 选择该日的成员（组内轮换）
            member = group_members[(assign_idx_start + d) % len(group_members)]

            new_schedule = DutySchedule(
                member_id=member.id,
                duty_date=duty_day,
                is_completed=False,
            )
            db.add(new_schedule)
            created.append(new_schedule)

        # 更新该组的轮换起始位置，确保连续周内继续轮换
        rotate_idx[group_grade] = (assign_idx_start + day_count) % len(group_members)

    if created:
        db.commit()
        # 刷新以便返回主键与关系
        for s in created:
            db.refresh(s)

    return {"data": created, "total": len(created)}
