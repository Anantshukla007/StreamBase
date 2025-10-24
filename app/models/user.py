# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# ----- ENUM for roles -----
class RoleEnum(str, enum.Enum):
    admin = "admin"
    creator = "creator"
    viewer = "viewer"


# ----- Association tables -----

# User <-> Video (Likes)
likes_table = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
)

# User <-> Video (Watch Later)
watch_later_table = Table(
    "watch_later",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
)

# Subscriptions: user can subscribe to other users
subscriptions_table = Table(
    "subscriptions",
    Base.metadata,
    Column("subscriber_id", ForeignKey("users.id"), primary_key=True),
    Column("subscribed_to_id", ForeignKey("users.id"), primary_key=True),
)


# ----- User model -----
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)

    # Relationships
    videos = relationship("Video", back_populates="uploader", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # Many-to-many relationships
    liked_videos = relationship("Video", secondary=likes_table, back_populates="liked_by")
    watch_later_videos = relationship("Video", secondary=watch_later_table, back_populates="watch_later_by")

    # Subscribers / Subscribed To (self-referential many-to-many)
    subscribers = relationship(
        "User",
        secondary=subscriptions_table,
        primaryjoin=id == subscriptions_table.c.subscribed_to_id,
        secondaryjoin=id == subscriptions_table.c.subscriber_id,
        back_populates="subscriptions",
    )

    subscriptions = relationship(
        "User",
        secondary=subscriptions_table,
        primaryjoin=id == subscriptions_table.c.subscriber_id,
        secondaryjoin=id == subscriptions_table.c.subscribed_to_id,
        back_populates="subscribers",
    )
