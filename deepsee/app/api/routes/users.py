from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep
) 
from app import models
from app.schemas import (
    UserCreate,
    UserUpdate,
    User,
    UserPublic,
)

router = APIRouter()


@router.get('/me', response_model=UserPublic)
def get_current_user(user: CurrentUser):
    return user


@router.put('/me/update', response_model=UserPublic)
def update_user(*, session: SessionDep, user: CurrentUser, user_in: UserUpdate):
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists.'
        )
    updated_user = crud.update_user(session=session, user=user, user_in=user_in)
    return updated_user


@router.delete('/me/delete')
def delete_user_account(*, session: SessionDep, user: CurrentUser):
    user_id = crud.delete_user(session=session, user=user)
    return {'success': f'User {user_id} deleted.'}


@router.post('/create', response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate):
    # ensure User does not exist
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists.'
        )
    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get('/{id}', response_model=UserPublic)
def read_user(*, id: int, session: SessionDep):
    user = session.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The user with the ID {id} does not exist.'
        )
    return user