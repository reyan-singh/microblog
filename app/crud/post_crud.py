from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post_models import Post
from app.models.user_models import User
from app.schemas.post_schemas import PostCreate
# app/crud/post_crud.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_timeline_posts(db: AsyncSession, *, current_user: User, skip: int = 0, limit: int = 20):
    """
    Gets posts from users that the current_user follows.
    """
    # Get IDs of users the current user is following
    followed_user_ids = [user.id for user in current_user.following]

    # Query for posts from those users
    result = await db.execute(
        select(Post)
        .filter(Post.owner_id.in_(followed_user_ids))
        .order_by(Post.id.desc())
        .options(selectinload(Post.owner)) # Eager load the owner to avoid N+1 queries
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_post(db: AsyncSession, *, post_in: PostCreate, owner_id: int) -> Post:
    """
    Creates a new post in the database.
    """
    db_post = Post(text=post_in.text, owner_id=owner_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def get_posts_by_user(db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 20) -> list[Post]:
    """
    Retrieves all posts for a specific user.
    """
    result = await db.execute(
        select(Post)
        .filter(Post.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Post.id.desc())
    )
    return result.scalars().all()