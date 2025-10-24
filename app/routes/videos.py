# app/routes/videos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.dependencies import get_db, get_current_user
from app.models.video import Video
from app.models.user import User, RoleEnum
from app.schemas.video_schema import VideoCreate, VideoRead, VideoDetail

router = APIRouter(prefix="/videos", tags=["Videos"])



@router.post("/",response_model =VideoRead,status_code=status.HTTP_201_CREATED)
async def upload_video(
    payload:VideoCreate,
    db:AsyncSession=Depends(get_db),
    current_user:User =Depends(get_current_user)

):
    if current_user.role not in [RoleEnum.creator,RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only creators or admins can upload videos")
    new_video = Video(
        title=payload.title,
        description=payload.description,
        video_url=str(payload.video_url),
        thumbnail_url=str(payload.thumbnail_url),
        uploader_id=current_user.id,
    )
    db.add(new_video)
    await db.commit()
    await db.refresh(new_video)
    return new_video


@router.get("/",response_model=list[VideoRead])
async def get_all_videos(db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Video))
    videos = result.scalars().all()
    return videos

@router.get("/uploader/{user_id}",response_model=list[VideoRead])
async def get_videos_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video)).where(Video.uploader_id == user_id)
    videos = result.scalars().all()
    return videos

@router.post("/{video_id}/like", response_model=dict)
async def like_unlike_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video in current_user.liked_videos:
        current_user.liked_videos.remove(video)
        action = "unliked"
    else:
        current_user.liked_videos.append(video)
        action = "liked"

    await db.commit()
    return {"message": f"Video {action} successfully"}

@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Permission check
    if current_user.role != RoleEnum.admin and video.uploader_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot delete this video")

    await db.delete(video)
    await db.commit()


@router.get("/{video_id}", response_model=VideoDetail)
async def get_video_details(video_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await db.refresh(video)
    return video
