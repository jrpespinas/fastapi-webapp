"""
This program is composed of the endpoints for the `Users` module.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, oauth2
from ..repository import user

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", response_model=schemas.ShowUser)
def create_user(
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user.create_user(request, db)


@router.get("/", response_model=List[schemas.ShowUser])
def get_all_users(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user.get_all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user.get_user_by_id(id, db)


@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user.delete_user_by_id(id, db)


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowSingleUser
)
def update_user(
    id: int,
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user.update_user_by_id(id, request, db)
