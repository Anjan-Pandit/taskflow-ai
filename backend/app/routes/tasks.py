from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import time

from ..database import get_db
from ..models import Task
from ..schemas import TaskCreate, TaskResponse
from ..utils.algorithms import (
    insertion_sort,
    linear_search,
    binary_search
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# ==========================================
# CREATE TASK
# ==========================================

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        project_id=task.project_id,
        priority=task.priority,
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==========================================
# GET ALL TASKS
# ==========================================

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    sort: str | None = Query(
        default=None,
        description="Sort by priority or due_date"
    ),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    # No sorting requested
    if not sort:
        return tasks

    # Convert tasks to dictionaries
    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "project_id": task.project_id,
            "priority": task.priority,
            "due_date": task.due_date
        }
        for task in tasks
    ]

    # ======================================
    # SORT BY PRIORITY
    # ======================================

    if sort == "priority":

        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3,
            "high": 1,
            "medium": 2,
            "low": 3
        }

        task_data = insertion_sort(
            task_data,
            key=lambda x: priority_order.get(
                x["priority"],
                2
            )
        )

    # ======================================
    # SORT BY DUE DATE
    # ======================================

    elif sort == "due_date":

        task_data = insertion_sort(
            task_data,
            key=lambda x: str(x["due_date"] or "")
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort option. Use priority or due_date."
        )

    return task_data


# ==========================================
# GET SINGLE TASK
# ==========================================

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# ==========================================
# UPDATE TASK
# ==========================================

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    task.project_id = task_data.project_id
    task.priority = task_data.priority
    task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task


# ==========================================
# DELETE TASK
# ==========================================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task_id": task_id
    }


# ==========================================
# LINEAR SEARCH
# ==========================================

@router.get("/search/linear")
def search_linear(
    title: str,
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    index = linear_search(
        tasks,
        title
    )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[index]


# ==========================================
# BINARY SEARCH
# ==========================================

@router.get("/search/binary")
def search_binary(
    title: str,
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found"
        )

    # Binary search ke liye title ke according sort
    tasks = sorted(
        tasks,
        key=lambda task: task.title.lower()
    )

    index = binary_search(
        tasks,
        title
    )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[index]


# ==========================================
# ALGORITHM BENCHMARK
# ==========================================

@router.get("/benchmark")
def benchmark_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "project_id": task.project_id,
            "priority": task.priority,
            "due_date": task.due_date
        }
        for task in tasks
    ]

    start_time = time.perf_counter()

    insertion_sort(
        task_data,
        key=lambda x: x["priority"]
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return {
        "algorithm": "Insertion Sort",
        "records_count": len(task_data),
        "execution_time_seconds": execution_time
    }