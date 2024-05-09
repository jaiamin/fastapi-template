from datetime import datetime

from pydantic import BaseModel, EmailStr


# Base class for Image
class ImageBase(BaseModel):
    uuid: str


# Create class for Image
class ImageCreate(ImageBase):
    pass


# Internal class for Image
class Image(ImageBase):
    id: int
    dataset_id: int

    class Config:
        from_attributes = True


# Public class for Image
class ImagePublic(ImageBase):
    pass


# Base class for Dataset
class DatasetBase(BaseModel):
    title: str
    tags: str


# Create class for Dataset
class DatasetCreate(DatasetBase):
    pass


# Internal class for Dataset
class Dataset(DatasetBase):
    id: int
    creation_date: datetime = datetime.now()
    user_id: int
    images: list[Image] = []

    class Config:
        from_attributes = True


# Public class for Dataset
class DatasetPublic(DatasetBase):
    creation_date: datetime = datetime.now()
    user_id: int
    images: list[Image] = []


# Base class for User
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


# Create class for User
class UserCreate(UserBase):
    password: str


# Internal class for User
class User(UserBase):
    id: int
    hashed_password: str
    datasets: list[Dataset] = []

    class Config:
        from_attributes = True


# Public class for User
class UserPublic(UserBase):
    datasets: list[Dataset] = []


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int | None = None