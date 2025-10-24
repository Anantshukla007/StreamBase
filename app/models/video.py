# app/models/video.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.user import likes_table, watch_later_table

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    uploader = relationship("User", back_populates="videos")
    comments = relationship("Comment", back_populates="video", cascade="all, delete-orphan")

    # Many-to-many
    liked_by = relationship("User", secondary=likes_table, back_populates="liked_videos")
    watch_later_by = relationship("User", secondary=watch_later_table, back_populates="watch_later_videos")
