from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Comment(Base):
    __tablename__ ="comments"

    id = Column(Integer,primary_key =True,index=True)
    content=Column(Text,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # ✅

    user_id =Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    video_id =Column(Integer,ForeignKey("videos.id",ondelete="CASCADE"))

    user = relationship("User",back_populates="comment")
    video =relationship("Video",back_populates="comments")