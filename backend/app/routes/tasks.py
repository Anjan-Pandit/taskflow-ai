from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..utils.algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# ==========================================
# CREATE TASK
# ==========================================

@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    return crud.create_task(db, task)


# ==========================================
# GET ALL TASKS
#
# Normal:
# /tasks/
#
# Priority:
# /tasks/?sort=priority
#
# Due Date:
# /tasks/?sort=due_date
# ==========================================

@router.get(
    "/",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    sort: str | None = Query(
        default=None,
        description="Sort by priority or due_date"
    ),
    db: Session = Depends(get_db)
):

    tasks = crud.get_tasks(db)

    # --------------------------------------
    # No sorting
    # --------------------------------------

    if sort is None:
        return tasks

    # --------------------------------------
    # Priority sorting
    # High -> Medium -> Low
    # --------------------------------------

    if sort == "priority":

        priority_rank = {
            "high": 0,
            "medium": 1,
            "low": 2
        }

        records = []

        for task in tasks:

            # Handle Enum priority
            priority_value = (
                task.priority.value
                if hasattr(task.priority, "value")
                else str(task.priority)
            )

            records.append({
                "task": task,
                "sort_value": priority_rank.get(
                    priority_value.lower(),
                    99
                )
            })

        # Use insertion sort
        insertion_sort(records, "sort_value")

        return [
            record["task"]
            for record in records
        ]

    # --------------------------------------
    # Due date sorting
    # Earliest first
    # --------------------------------------

    if sort == "due_date":

        records = []

        for task in tasks:

            if task.due_date:
                due_value = str(task.due_date)
            else:
                # No due date -> last
                due_value = "9999-12-31"

            records.append({
                "task": task,
                "sort_value": due_value
            })

        # Use insertion sort
        insertion_sort(records, "sort_value")

        return [
            record["task"]
            for record in records
        ]

    # --------------------------------------
    # Invalid sort option
    # --------------------------------------

    raise HTTPException(
        status_code=400,
        detail="Invalid sort option. Use priority or due_date."
    )


# ==========================================
# SEARCH TASK
#
# Linear:
# /tasks/search?title=Learn%20FastAPI&algo=linear
#
# Binary:
# /tasks/search?title=Learn%20FastAPI&algo=binary
# ==========================================

@router.get(
    "/search",
    response_model=schemas.TaskResponse
)
def search_task(
    title: str,
    algo: str = Query(
        default="linear",
        description="Search algorithm: linear or binary"
    ),
    db: Session = Depends(get_db)
):

    tasks = crud.get_tasks(db)

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    target = title.strip().lower()

    # ======================================
    # LINEAR SEARCH
    # ======================================

    if algo == "linear":

        records = []

        for task in tasks:

            records.append({
                "task": task,
                "title": str(task.title).lower()
            })

        index = linear_search(
            records,
            target,
            "title"
        )

        if index == -1:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return records[index]["task"]

    # ======================================
    # BINARY SEARCH
    # ======================================

    if algo == "binary":

        records = []

        for task in tasks:

            records.append({
                "task": task,
                "title": str(task.title).lower()
            })

        # Binary search needs sorted data.
        # Sort titles first using insertion sort.
        insertion_sort(records, "title")

        index = binary_search(
            records,
            target,
            "title"
        )

        if index == -1:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return records[index]["task"]

    # ======================================
    # INVALID SEARCH ALGORITHM
    # ======================================

    raise HTTPException(
        status_code=400,
        detail="Invalid algorithm. Use linear or binary."
    )


# ==========================================
# GET SINGLE TASK
# ==========================================

@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = crud.get_task(
        db,
        task_id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# ==========================================
# UPDATE TASK
# ==========================================

@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):

    updated_task = crud.update_task(
        db,
        task_id,
        task
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


# ==========================================
# DELETE TASK
# ==========================================

@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    deleted_task = crud.delete_task(
        db,
        task_id
    )

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }