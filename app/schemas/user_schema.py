from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    creator = "creator"
    viewer = "viewer"

# ---------- Base ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

# ---------- Create ----------
class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.viewer

# ---------- Read ----------
class UserRead(UserBase):
    id: int
    role: RoleEnum

    class Config:
        from_attributes = True

# ---------- With Relations ----------
class UserDetail(UserRead):
    uploaded_videos: Optional[List["VideoRead"]] = []
    liked_videos: Optional[List["VideoRead"]] = []
    watch_later_videos: Optional[List["VideoRead"]] = []
    subscribers: Optional[List["UserRead"]] = []
    subscriptions: Optional[List["UserRead"]] = []

# ---------- Resolve Forward References ----------
from app.schemas.video_schema import VideoRead  # imported here to avoid circular import

UserDetail.model_rebuild()
