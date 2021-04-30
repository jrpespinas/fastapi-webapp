from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import models
from ..security import Hashing

def create_user(request, db):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hashing.get_hash_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id, db):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available!",
        )

    return user