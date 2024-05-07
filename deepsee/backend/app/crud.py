from sqlalchemy.orm import Session, select

from .core.security import get_password_hash, verify_password
from .schemas import UserCreate, User, DatasetCreate, Dataset, ImageCreate, Image


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={'hashed_password': get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.execute(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return None


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