from fastapi import APIRouter

from .routes import login, users, datasets, images

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(datasets.router, prefix='/datasets', tags=['datasets'])
api_router.include_router(images.router, prefix='/images', tags=['images'])