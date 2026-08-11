
from sqlalchemy.orm import Session

from . import models, schemas


# CREATE
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        project_id=task.project_id,
        priority=task.priority,
        due_date=task.due_date
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# READ - All Tasks
def get_tasks(db: Session):
    return db.query(models.Task).all()


# READ - Single Task
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()


# UPDATE
def update_task(
    db: Session,
    task_id: int,
    task: schemas.TaskCreate
):
    db_task = get_task(db, task_id)

    if db_task is None:
        return None

    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db_task.project_id = task.project_id
    db_task.priority = task.priority
    db_task.due_date = task.due_date

    db.commit()
    db.refresh(db_task)

    return db_task


# DELETE
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)

    if db_task is None:
        return None

    db.delete(db_task)
    db.commit()

    return db_task

