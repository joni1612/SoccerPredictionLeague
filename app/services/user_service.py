from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.core.security import create_access_token, hash_password, verify_password
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
        inner = getattr(e.orig, "__cause__", None)
        constraint = getattr(inner, "constraint_name", "") or ""
        if "email" in constraint:
            raise ConflictError("Email already registered")
        if "username" in constraint:
            raise ConflictError("Username already taken")
        raise ConflictError("User already exists")


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
    user = await authenticate_user(db, email, password)
    if not user:
        return None
    user.token_version += 1
    await db.commit()
    return create_access_token(str(user.id), user.token_version)
