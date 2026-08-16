from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):

    title: str

    description: str = ""

    completed: bool = False

    # PROJECT ID IS OPTIONAL
    project_id: int | None = None

    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )

    due_date: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        if not value.strip():
            raise ValueError(
                "Title cannot be blank"
            )

        return value.strip()


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):

    id: int

    class Config:
        from_attributes = True