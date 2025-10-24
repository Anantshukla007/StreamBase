from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

# ---------- Base ----------
class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: HttpUrl
    thumbnail_url: Optional[HttpUrl] = None

# ---------- Create ----------
class VideoCreate(VideoBase):
    pass

# ---------- Read ----------
class VideoRead(VideoBase):
    id: int
    upload_time: datetime
    uploader_id: int

    class Config:
        from_attributes = True

# ---------- With Relations ----------
class VideoDetail(VideoRead):
    uploader: Optional["UserRead"]
    comments: Optional[List["CommentRead"]] = []
    liked_by: Optional[List["UserRead"]] = []
    watch_later_by: Optional[List["UserRead"]] = []

# ---------- Resolve Forward References ----------
from app.schemas.user_schema import UserRead
from app.schemas.comment_schema import CommentRead

VideoDetail.model_rebuild()
