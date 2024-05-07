from datetime import datetime

from pydantic import BaseModel, EmailStr


class ImageBase(BaseModel):
    uuid: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    dataset_id: int

    class Config:
        orm_mode = True


class DatasetBase(BaseModel):
    title: str
    tags: str


class DatasetCreate(DatasetBase):
    pass


class Dataset(DatasetBase):
    id: int
    creation_date: datetime = datetime.now()
    user_id: int
    images: list[Image] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    datasets: list[Dataset] = []

    class Config:
        orm_mode = True


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int | None = None