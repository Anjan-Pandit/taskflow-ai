from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
def create_project(
    name: str,
    owner_id: int,
    db: Session = Depends(get_db)
):
    owner = db.query(models.User).filter(
        models.User.id == owner_id
    ).first()

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project = models.Project(
        name=name,
        owner_id=owner_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/")
def get_projects(
    db: Session = Depends(get_db)
):
    return db.query(models.Project).all()


@router.get("/stats")
def get_project_stats(
    db: Session = Depends(get_db)
):
    stats = (
        db.query(
            models.Project.id.label("project_id"),
            models.Project.name.label("project_name"),
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(
            models.Task,
            models.Project.id == models.Task.project_id
        )
        .group_by(
            models.Project.id,
            models.Project.name
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count
        }
        for row in stats
    ]