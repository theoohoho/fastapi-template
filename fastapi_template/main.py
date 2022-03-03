from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.router import api_router
from .api.events import startup_app_handler, shutdown_app_handler
from .core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.include_router(api_router, prefix="/api")

app.add_event_handler("startup", startup_app_handler)
app.add_event_handler("shutdown", shutdown_app_handler)
# Set all CORS enabled origins
if settings.cors_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
