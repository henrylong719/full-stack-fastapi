from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger("app.main")


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    logger.info("Environment: %s", settings.ENVIRONMENT)
    logger.info("API prefix: %s", settings.API_V1_STR)
    logger.info(
        "CORS origins (%d): %s",
        len(settings.all_cors_origins),
        settings.all_cors_origins,
    )
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Optional lightweight request logging middleware (good for local dev)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    if settings.is_local:
        logger.info(
            "%s %s -> %s", request.method, request.url.path, response.status_code
        )
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
