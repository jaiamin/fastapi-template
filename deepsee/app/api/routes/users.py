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
def get_current_user(current_user: CurrentUser):
    return current_user


@router.put('/me/update', response_model=UserPublic)
def update_user(*, session: SessionDep, current_user: CurrentUser, user_in: UserUpdate):
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This email is already registered.'
        )
    updated_user = crud.update_user(session=session, uid=current_user.id, user_in=user_in)
    return updated_user


@router.delete('/me/delete')
def delete_user_account(*, session: SessionDep, current_user: CurrentUser):
    user_id = crud.delete_user(session=session, uid=current_user.id)
    return {'success': f'User {user_id} deleted.'}


@router.post('/create', response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate):
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This email is already registered.'
        )
    new_user = crud.create_user(session=session, user_in=user_in)
    return new_user


@router.get('/{id}', response_model=UserPublic)
def read_user(*, id: int, session: SessionDep):
    user = crud.get_user(session=session, uid=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The user with the ID {id} does not exist.'
        )
    return user