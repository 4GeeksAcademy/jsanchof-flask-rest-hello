from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Followers(db.Model):
    user_from_id : Mapped[int] = mapped_column(Integer,ForeignKey('user.id'),nullable=False)
    user_to_id : Mapped[int] = mapped_column(Integer,ForeignKey('user.id'),nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_from_id', 'user_to_id'),)  # Composite primary key

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
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

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

class Commet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    commet_text: Mapped[str] = mapped_column(String(120), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "commet_text": self.commet_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }