from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError as e:
        await db.rollback()
        # SQLAlchemy wraps asyncpg in an adapter; the real exception is in __cause__
        inner = getattr(e.orig, "__cause__", None)
        constraint = getattr(inner, "constraint_name", "") or ""
        if "email" in constraint:
            raise HTTPException(status_code=409, detail="Email already registered")
        if "username" in constraint:
            raise HTTPException(status_code=409, detail="Username already taken")
        raise HTTPException(status_code=409, detail="User already exists")
