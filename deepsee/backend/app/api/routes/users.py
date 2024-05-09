from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import delete, func, select

from deepsee.backend.app import crud
from deepsee.backend.app.api.deps import (
    CurrentUser,
    SessionDep
)
from deepsee.backend.app.core.config import settings
from deepsee.backend.app.core.security import get_password_hash, verify_password
from deepsee.backend.app import models
from deepsee.backend.app.schemas import (
    UserCreate,
)

router = APIRouter()


@router.get('/')
def read_users(*, session: SessionDep, skip: int = 0, limit: int = 100):
    """
    Retrieve users.
    """
    users = session.query(models.User).offset(skip).limit(limit).all()
    return users


@router.post('/')
def create_user(*, session: SessionDep, user_in: UserCreate):
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    print('USER USER USER USER USER :::::', user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    return user