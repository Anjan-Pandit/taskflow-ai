from fastapi import APIRouter
from pydantic import BaseModel

from ..ai import analyze_task


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AIQuickAddRequest(BaseModel):
    title: str
    description: str = ""


@router.post("/analyze-task")
def analyze_task_api(request: AIQuickAddRequest):
    return analyze_task(
        request.title,
        request.description
    )