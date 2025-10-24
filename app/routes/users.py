# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.video import Video
from app.schemas.user_schema import UserRead, UserDetail

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/me",response_model=UserDetail)
async def get_my_profile(current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await db.refresh(current_user)
    return current_user

@router.post("/{user_id}/subscribe",response_model="UserRead")
async def subscribe_to_user(
    user_id:int,
    current_user:User = Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    if current_user.id  == user_id:
        raise HTTPException(status_code=400, detail="You cannot subscribe to yourself")
    result = await db.execute(select(User)).where(User.id==user_id)
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user in current_user.subscriptions:
        raise HTTPException(status_code=400, detail="Already subscribed")
    current_user.subscriptions.append(target_user)
    await db.commit()
    return target_user

@router.delete("/{user_id}/unsubscribe",status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_from_user(
    user_id:int,
    current_user:User = Depends(get_current_user),
    db:AsyncSession= Depends(get_db)
):
    result = await db.execute(select(User)).where(User.id == user_id)
    target_user= result.scalar_one_or_none
    if not target_user:
        raise HTTPException(status_code=404,detail="user not found")
    if target_user not in current_user.subscriptions:
        raise HTTPException(status_code=400, detail="You are not subscribed")

    current_user.subscriptions.remove(target_user)
    await db.commit()


@router.get("/{user_id}/subscribers", response_model=list[UserRead])
async def get_user_subscribers(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.refresh(user)
    return user.subscribers

@router.get("/{user_id}/subscribers", response_model=list[UserRead])
async def get_user_subscribers(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.refresh(user)
    return user.subscribers


@router.post("/watchlater/{video_id}",response_model=dict)
async def toggle_watch_later(
    video_id:int,
    current_user:User =Depends(get_current_user),
    db:AsyncSession =Depends(get_db)
):
    result = await db.execute(select(Video)).where(Video.id==video_id)
    video = result.scalar_one_or_none
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if video in current_user.watch_later_videos:
        current_user.watch_later_videos.remove(video)
        action ="removed"
    else:
        current_user.watch_later_videos.append(video)
        action ="added"
    await db.commit()
    return {"message" :f"Video {action} to wathc later list"}
