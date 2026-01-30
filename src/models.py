from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from typing import List
import enum

db = SQLAlchemy()


class MediaType(enum.Enum):
    photo = "photo"
    video = "video"
    gif = "gif"


  

class User(db.Model):
    __tablename__="user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)



class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
 
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
   
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False) 
   
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) 

 

   
  

 