from fastapi import APIRouter

from .routes import users, items

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(items.router)