from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models.comment import Comment
from app.models.video import Video
from app.models.user import User, RoleEnum
from app.schemas.comment_schema import CommentCreate, CommentRead
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def add_comment(
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the video exists
    result = await db.execute(select(Video).where(Video.id == payload.video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    comment = Comment(
        text=payload.text,
        video_id=payload.video_id,
        user_id=current_user.id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment



@router.get("/video/{video_id}", response_model=list[CommentRead])
async def get_comments_for_video(video_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment).where(Comment.video_id == video_id).order_by(Comment.created_at.desc())
    )
    return result.scalars().all()


@router.get("/user/{user_id}", response_model=list[CommentRead])
async def get_comments_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment).where(Comment.user_id == user_id).order_by(Comment.created_at.desc())
    )
    return result.scalars().all()


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.role != RoleEnum.admin and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    await db.delete(comment)
    await db.commit()

@router.put("/{comment_id}", response_model=CommentRead)
async def edit_comment(
    comment_id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own comments")

    comment.text = payload.text
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/video/{video_id}/stats", response_model=dict)
async def get_comment_stats(video_id: int, db: AsyncSession = Depends(get_db)):
    total_comments_query = await db.execute(
        select(func.count(Comment.id)).where(Comment.video_id == video_id)
    )
    total_comments = total_comments_query.scalar()

    latest_comment_query = await db.execute(
        select(Comment).where(Comment.video_id == video_id).order_by(Comment.created_at.desc()).limit(1)
    )
    latest_comment = latest_comment_query.scalar_one_or_none()

    return {
        "video_id": video_id,
        "total_comments": total_comments,
        "latest_comment": latest_comment.text if latest_comment else None,
        "latest_comment_time": latest_comment.created_at if latest_comment else None
    }
