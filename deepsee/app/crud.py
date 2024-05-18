from enum import Enum
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app import models
from app.enums import DatasetType
from app.schemas import (
    UserCreate,
    UserUpdate, 
    DatasetCreate, 
    ImageCreate,
)


def get_user(*, session: Session, uid: int) -> models.User | None:
    """Returns a user based on the given user id."""
    return session.query(models.User).filter(models.User.id == uid).one_or_none()


def get_user_by_email(*, session: Session, email: str) -> models.User | None:
    """Returns a user based on the given email."""
    return session.query(models.User).filter(models.User.email == email).one_or_none()


def create_user(*, session: Session, user_in: UserCreate) -> models.User:
    """Creates a new deepsee user."""
    hashed_password = get_password_hash(user_in.password)
    user = models.User(
        **user_in.model_dump(exclude={'password'}), hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    return user


def update_user(*, session: Session, uid: int, user_in: UserUpdate) -> models.User | None:
    """Update an existing deepsee user."""
    user = get_user(session=session, uid=uid)
    if not user:
        return None
    
    # update user attributes
    update_data = user_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(user, k, v)

    session.commit()
    session.refresh(user)
    return user


def delete_user(*, session: Session, uid: int) -> int:
    """Delete an existing deepsee user."""
    user = get_user(session=session, uid=uid)
    if not user:
        return None
    
    session.delete(user)
    session.commit()
    return user.id


def authenticate(*, session: Session, email: str, password: str) -> models.User | None:
    """Authenticates a deepsee user."""
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



def get_dataset_by_title(*, session: Session, dataset_title: str) -> models.Dataset | None:
    """Returns a deepsee dataset based on the given dataset title."""
    return session.query(models.Dataset).filter(models.Dataset.title == dataset_title).one_or_none()


def get_datasets(*, session: Session) -> list[models.Dataset]:
    """Retrieve all datasets stored on deepsee."""
    return session.query(models.Dataset).all()


def get_user_datasets(*, session: Session, uid: int) -> list[models.Dataset]:
    """Retrieve a user's datasets stored on deepsee."""
    return session.query(models.Dataset).filter(models.Dataset.user_id == uid).all()


def create_dataset(*, session: Session, dataset_in: DatasetCreate, uid: int) -> models.Dataset:
    """Create a new dataset associated with a user."""
    dataset = models.Dataset(
        title=dataset_in.title,
        tags=dataset_in.tags,
        user_id=uid, 
    )
    session.add(dataset)
    session.commit()
    return dataset


def create_image(*, session: Session, image_in: ImageCreate, dataset_id: int) -> models.Image:
    """Create a new image associated with a dataset."""
    image = models.Image(
        **image_in.model_dump(), dataset_id=dataset_id
    )
    session.add(image)
    session.commit()
    return image