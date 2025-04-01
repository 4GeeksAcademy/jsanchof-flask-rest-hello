from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, PrimaryKeyConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#relationship  M <-> M
likes = Table('likes', db.Model.metadata,
              Column('user_id',Integer, ForeignKey('user.id', primary_key = True)),
              Column('post_id',Integer, ForeignKey('post.id', primary_key = True)))

class Followers(db.Model):
    user_from_id : Mapped[int] = mapped_column(Integer,ForeignKey('user.id'),nullable=False)
    user_to_id : Mapped[int] = mapped_column(Integer,ForeignKey('user.id'),nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_from_id', 'user_to_id'),)  # Composite primary key
    #relationships
    

    def serialize(self):
        return{
            "user_from_id":self.user_from_id,
            "user_to_id":self.user_to_id
        }

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    #relationships
    post: Mapped[list["Post"]] = relationship('Post', back_populates = 'user'),
    liked_posts: Mapped[list["Post"]] = relationship('Post', secondary=likes, back_populates = 'user'),
    comment: Mapped[list["Comment"]] = relationship('Comment', back_populates = 'liking_users')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_text: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
#relationships 
    user: Mapped["User"] = relationship('User', back_populates='posts')
    comments: Mapped[list["Comment"]] = relationship('Comment', back_populates='posts')
    linking_users: Mapped[list["User"]] = relationship('User', secondary=likes, back_populates='liked_posts')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(15), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    commet_text: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    #relationships
    user: Mapped["User"] = relationship('User', back_populates='comments')
    post: Mapped["Post"] = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "commet_text": self.commet_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }