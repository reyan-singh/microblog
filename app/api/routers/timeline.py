import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user, get_db
from app.core.redis_client import redis_client
from app.models.user_models import User
from app.crud import post_crud
from app.schemas.post_schemas import PostInDB

router = APIRouter()

@router.get("/", response_model=List[PostInDB])
async def get_timeline(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cache_key = f"timeline:{current_user.id}"

    # 1. Try to get from cache
    cached_timeline = await redis_client.get(cache_key)
    if cached_timeline:
        return json.loads(cached_timeline)

    # 2. If cache miss, get from DB
    timeline_posts = await post_crud.get_timeline_posts(db=db, current_user=current_user)

    # Convert SQLAlchemy models to dicts for JSON serialization
    posts_as_dicts = [PostInDB.from_orm(post).dict() for post in timeline_posts]

    # 3. Set to cache for 1 minute
    await redis_client.set(cache_key, json.dumps(posts_as_dicts), ex=60)

    return posts_as_dicts