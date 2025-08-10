from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user, get_db
from app.models.user_models import User
from app.crud import user_crud

router = APIRouter()

@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_a_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    result = await user_crud.follow_user(db, follower=current_user, followed_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User to follow not found")

@router.post("/{user_id}/unfollow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_a_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await user_crud.unfollow_user(db, follower=current_user, followed_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User to unfollow not found or you were not following them")