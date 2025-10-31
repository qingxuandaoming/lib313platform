from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.project import Project, ProjectMember
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()


@router.get("", response_model=List[ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """获取单个项目详情"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    return project


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """创建新项目"""
    project_data = project.model_dump(exclude={'member_ids'})
    db_project = Project(**project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # 添加项目成员
    if project.member_ids:
        for member_id in project.member_ids:
            project_member = ProjectMember(
                project_id=db_project.id,
                member_id=member_id
            )
            db.add(project_member)
        db.commit()

    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """更新项目信息"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )

    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """删除项目"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )

    db.delete(db_project)
    db.commit()
    return None


@router.post("/{project_id}/members/{member_id}", status_code=status.HTTP_201_CREATED)
def add_project_member(
    project_id: int,
    member_id: int,
    role: str = None,
    db: Session = Depends(get_db)
):
    """添加项目成员"""
    # 检查项目和成员是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 检查是否已经是成员
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.member_id == member_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="成员已在项目中")

    project_member = ProjectMember(
        project_id=project_id,
        member_id=member_id,
        role=role
    )
    db.add(project_member)
    db.commit()
    return {"message": "成员添加成功"}


@router.delete("/{project_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project_member(
    project_id: int,
    member_id: int,
    db: Session = Depends(get_db)
):
    """移除项目成员"""
    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.member_id == member_id
    ).first()
    if not project_member:
        raise HTTPException(status_code=404, detail="项目成员关系不存在")

    db.delete(project_member)
    db.commit()
    return None
