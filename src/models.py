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

    users: Mapped[list ['Follower']]= relationship(Follower) back_populates: "user"
 
    following: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys=[Follower.user_from_id], 
        back_populates="follower_from"
    )

    followers_of: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys=[Follower.user_to_id], # La FK que pertenece a este lado
        back_populates="follower_to"
    )

    # NUEVA RELACIÓN: un usuario tienen muchos posts:


    posts: Mapped[List["Post"]] = relationship(
        "Post", 
        back_populates="author",
        cascade="all, delete-orphan"
    )

     # NUEVA RELACIÓN**: Un usuario hace muchos comentarios (1:N)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author", cascade="all, delete-orphan")




class Follower(db.Model):
    __tablename__="follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
   
    from_user: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    to_user: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers_of")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

   


class Comment(db.Model):
    __tablename__="comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    


class Post(db.Model):
    __tablename__="post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

     # **NUEVA RELACIÓN: un post pertenece a 1 solo autor
    author: Mapped["User"] = relationship("User", back_populates="posts")
   
    media_items: Mapped[List["Media"]] = relationship(
        "Media",
        back_populates="post",
        cascade="all, delete-orphan"
    )
   
  # NUEVA RELACIÓN: Un post tiene muchos comentarios (1:N)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")



class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType, name="media_type_enum"),
        nullable=False
    )
    url: Mapped[str] = mapped_column(String(255)) 
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id")) 
    
    post: Mapped["Post"] = relationship("Post", back_populates="media_items")

 

   
  

 