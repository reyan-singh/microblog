from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.post_schemas import PostCreate, PostInDB
from app.models.user_models import User
from app.crud import post_crud
from app.core.security import get_current_user
from app.api.routers.auth import get_db # Or use the shared get_db from security.py
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=PostInDB, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    *,
    db: AsyncSession = Depends(get_db),
    post_in: PostCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new post. The user must be logged in.
    [cite_start]The post text cannot be longer than 64 characters[cite: 3, 17].
    """
    if len(post_in.text) > 64: # Double-check even though Pydantic does it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post is too long. Maximum 64 characters allowed."
        )
    return await post_crud.create_post(db=db, post_in=post_in, owner_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[PostInDB])
async def read_user_posts(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int
):
    """
    [cite_start]Retrieve all posts from a specific user[cite: 22].
    """
    posts = await post_crud.get_posts_by_user(db=db, user_id=user_id)
    return posts