from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.database.session import engine, verify_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await verify_database_connection()
    yield
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(api_v1_router)
