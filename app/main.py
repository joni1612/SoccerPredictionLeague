from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, verify_database_connection
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    await verify_database_connection()
    yield
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(health.router)
