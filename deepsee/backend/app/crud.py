from sqlalchemy import select
from sqlalchemy.orm import Session

from .core.security import get_password_hash, verify_password
from . import models
from .schemas import (
    User,
    UserCreate, 
    DatasetCreate, 
    Dataset, 
    ImageCreate, 
    Image
)


def create_user(*, session: Session, user_create: UserCreate) -> models.User:
    db_obj = models.User(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete_user(*, session: Session, user: User) -> int:
    db_obj = models.User(**user.__dict__)
    session.delete(db_obj)
    session.commit()
    return db_obj.id


def get_user_by_email(*, session: Session, email: str) -> models.User | None:
    statement = select(models.User).where(models.User.email == models.User)
    session_user = session.execute(statement).first()
    if not session_user:
        return None
    return session_user[0]


def authenticate(*, session: Session, email: str, password: str) -> models.User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_dataset(*, session: Session, ds_in: DatasetCreate, user_id: int) -> Dataset:
    db_ds = Dataset.model_validate(ds_in, update={'user_id': user_id})
    session.add(db_ds)
    session.commit()
    session.refresh(db_ds)
    return db_ds


def create_image(*, session: Session, image_in: ImageCreate, dataset_id: int) -> Image:
    db_image = Image.model_validate(image_in, update={'dataset_id': dataset_id})
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image


def get_num_datasets(*, session: Session):
    return session.query(models.Dataset).count()


def get_num_users(*, session: Session):
    return session.query(models.User).count()


def get_num_images(*, session: Session):
    return session.query(models.Image).count()