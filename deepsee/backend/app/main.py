import time

from fastapi import (
    FastAPI, 
    Request
)
from starlette.middleware.cors import CORSMiddleware

from . import crud
from .api.deps import SessionDep
from .api.main import api_router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/documentation',
    redoc_url=None,
)

app.include_router(api_router)

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


@app.get('/')
def get_home_page(*, session: SessionDep):
    return {
        'title': 'DeepSee',
        'description': 'DeepSee is a collaborative platform for creating and sharing open-source computer vision datasets.',
        'stats': {
            'num_datasets': crud.get_num_datasets(session=session),
            'num_users': crud.get_num_users(session=session),
            'num_images': crud.get_num_images(session=session),
        }
    }