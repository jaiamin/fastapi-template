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
    User,
    UserPublic,
)

router = APIRouter()


@router.get('/me', response_model=UserPublic)
def get_current_user(user: CurrentUser):
    return user


@router.put('/me/update')
def update_user(*, session: SessionDep, user: CurrentUser, user_in):
    pass


@router.delete('/me/delete')
def delete_user(*, session: SessionDep, user: CurrentUser):
    user_id = delete_user(session=session, user=user)
    return {'success': f'User {user_id} deleted.'}


@router.post('/create', response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate):
    # ensure User does not exist
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in DeepSee.'
        )
    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get('/{id}', response_model=UserPublic)
def read_user(*, id: int, session: SessionDep):
    user = session.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The user with the ID "{id}" does not exist.'
        )
    return user