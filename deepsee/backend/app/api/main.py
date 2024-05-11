from fastapi import APIRouter

from .routes import auth, users, datasets

api_router = APIRouter()
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(datasets.router, prefix='/datasets', tags=['datasets'])