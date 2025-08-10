from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post_models import Post
from app.models.user_models import User
from app.schemas.post_schemas import PostCreate

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