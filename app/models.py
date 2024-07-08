from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    posts = relationship(
        "app.models.PostDB", back_populates="owner", cascade="all, delete-orphan"
    )
    __table_args__ = {"extend_existing": True}


class PostDB(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner = relationship("app.models.UserDB", back_populates="posts")
    __table_args__ = {"extend_existing": True}


class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=True,
    )
    # id_post = relationship("app.models.Post", overlaps="id_post")
    # id_user = relationship("app.models.User", overlaps="id_user")
    __table_args__ = {"extend_existing": True}
