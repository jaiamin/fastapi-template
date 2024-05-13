import time

from fastapi import (
    FastAPI, 
    Request
)
from starlette.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.deps import SessionDep
from app.api.main import api_router
from app.core.config import settings
from app.core.rate_limiter import limiter
from app.stats import get_stats


def get_application():
    application = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url='/documentation',
        redoc_url=None,
    )
    # rate limiting
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip('/') for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


    @application.middleware('http')
    async def db_session_middleware(request: Request, call_next):
        """
        Calculate process time.
        """
        start_time = time.time()  
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response


    @application.get('/')
    def get_home_page(*, session: SessionDep):
        return {
            'title': 'DeepSee',
            'description': 'DeepSee is a collaborative platform for creating and sharing open-source computer vision datasets.',
            'stats': get_stats(session=session)
        }


    @application.get('/ping')
    def ping():
        return "pong"


    application.include_router(api_router)

    return application


app = get_application()