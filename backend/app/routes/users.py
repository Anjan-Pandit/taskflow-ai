from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    email: str,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = models.User(email=email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(models.User).all()