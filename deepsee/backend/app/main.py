import time

from fastapi import (
    FastAPI, 
    Request
)
from starlette.middleware.cors import CORSMiddleware

from .api.main import api_router
from .models import Base
from .db import engine
from .core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/documentation',
    redoc_url=None,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip('/') for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    """
    Calculate process time.
    """
    start_time = time.time()  
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response
    

app.include_router(api_router)