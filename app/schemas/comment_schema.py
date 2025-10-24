from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------- Base ----------
class CommentBase(BaseModel):
    content: str

# ---------- Create ----------
class CommentCreate(CommentBase):
    video_id: int

# ---------- Read ----------
class CommentRead(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    video_id: int

    class Config:
        from_attributes = True
