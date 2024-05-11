from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from deepsee.backend.app.core.security import reusable_oauth2
from deepsee.backend.app import models
from deepsee.backend.app.core.config import settings
from deepsee.backend.app.core.db import get_local_session
from deepsee.backend.app.schemas import TokenPayload, User


def get_db() -> Generator[Session, None, None]:
    db = get_local_session(str(settings.SQLALCHEMY_DATABASE_URI), echo=False)()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(models.User, token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]