from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.hashing import get_password_hash
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(db: AsyncSession, user_id: int):
    # CORRECTED QUERY: Eagerly load relationships to prevent lazy loading errors
    result = await db.execute(
        select(User)
        .options(selectinload(User.following), selectinload(User.followers))
        .filter(User.id == user_id)
    )
    return result.scalars().first()

async def follow_user(db: AsyncSession, *, follower: User, followed_id: int):
    user_to_follow = await get_user_by_id(db, user_id=followed_id)
    if not user_to_follow:
        return None
    follower.following.append(user_to_follow)
    db.add(follower)
    await db.commit()
    return follower

async def unfollow_user(db: AsyncSession, *, follower: User, followed_id: int):
    user_to_unfollow = await get_user_by_id(db, user_id=followed_id)
    if not user_to_unfollow:
        return None
    try:
        follower.following.remove(user_to_unfollow)
        db.add(follower)
        await db.commit()
        return follower
    except ValueError:
        return None