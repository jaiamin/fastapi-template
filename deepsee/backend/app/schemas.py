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
        from_attributes = True


class ImagePublic(ImageBase):
    id: int


class ImagesPublic(BaseModel):
    data: list[ImagePublic]
    count: int


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
        from_attributes = True


class DatasetPublic(DatasetBase):
    id: int
    user_id: int


class DatasetsPublic(BaseModel):
    data: list[DatasetPublic]
    count: int


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    datasets: list[Dataset] = []

    class Config:
        from_attributes = True


# Properties to return via API, id always required
class UserPublic(UserBase):
    id: int


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int | None = None