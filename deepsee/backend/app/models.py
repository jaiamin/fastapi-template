from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String,
    DateTime,
    Enum
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from .core.base_class import Base
from .utils import DatasetType


class User(Base):
    """
    Represents a DeepSee User.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    datasets = relationship('Dataset', back_populates='user')


class Dataset(Base):
    """
    Represents a DeepSee Dataset created by a User.
    """
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    creation_date = Column(DateTime, server_default=func.now())
    tags = Column(Enum(DatasetType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='datasets')
    images = relationship('Image', back_populates='dataset')


class Image(Base):
    """
    Represents a pixel Image in a given Dataset.
    """
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))

    dataset = relationship('Dataset', back_populates='images')
