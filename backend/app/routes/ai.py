from fastapi import APIRouter

from ..ai import analyze_task


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/analyze-task")
def analyze_task_api(
    title: str,
    description: str
):
    return analyze_task(title, description)