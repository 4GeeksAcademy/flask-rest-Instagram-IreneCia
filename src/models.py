from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum, ForeignKey, Column, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()


class MediaType(enum.Enum):
    photo = "photo"
    video = "video"
    gif = "gif"



Follower = Table(
    "follower",
    db.metadata,

    Column(
        'user_from_id',
        Integer,
        ForeignKey('user.id'),
        primary_key=True
    ),
     Column(
        'user_to_id',
        Integer,
        ForeignKey('user.id'),
        primary_key=True
    )
)
  

class User(db.Model):
    __tablename__="user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

     # Relación

    following: Mapped[List["User"]] = relationship(
    "User",
    secondary=Follower,
    back_populates="followers"
    )

    followers: Mapped[List["User"]] = relationship(
    "User",
    secondary=Follower,
    back_populates="following"
    )

    # Relaciones con comments y post

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")



class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
   
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)


    # Relación con user
    user: Mapped["User"] = relationship("User", back_populates="posts")

     # Relación con media
    media_items: Mapped[List["Media"]] = relationship(
        "Media", 
        back_populates="post",
    )

    # Relación con Comments 
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False) 
   
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) 

     # Relación

    post: Mapped["Post"] = relationship("Post", 
        back_populates="media_items")

 

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
 
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)


      # Relaciones con post y user

    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    
    author: Mapped["User"] = relationship("User", back_populates="comments")

 