from wakuwaku.extensions import db

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.sql import text, func
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Account(UserMixin, db.Model):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.current_timestamp(), nullable=False
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    # This method is required by Flask-Login to know the unique identifier for the user.
    def get_id(self):
        return self.account_id


class Post(db.Model):
    __tablename__ = "post"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, ForeignKey("account.account_id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255))
    score = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.current_timestamp(), nullable=False
    )

    account = relationship("Account", backref=db.backref("posts", lazy=True))


class Image(db.Model):
    __tablename__ = "image"

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, ForeignKey("post.post_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    preview_url = db.Column(db.String(255), nullable=False)
    sample_url = db.Column(db.String(255), nullable=False)
    original_url = db.Column(db.String(255), nullable=False)

    post = relationship("Post", backref=db.backref("images", lazy=True))


class Tag(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class PostTag(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, ForeignKey("post.post_id"), primary_key=True)
    tag_id = db.Column(db.Integer, ForeignKey("tag.tag_id"), primary_key=True)

    post = relationship("Post", backref=db.backref("post_tags", lazy=True))
    tag = relationship("Tag", backref=db.backref("post_tags", lazy=True))


class Comment(db.Model):
    __tablename__ = "comment"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, ForeignKey("post.post_id"), nullable=False)
    account_id = db.Column(db.Integer, ForeignKey("account.account_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.current_timestamp(), nullable=False
    )

    account = relationship("Account", backref=db.backref("comments", lazy=True))
    post = relationship("Post", backref=db.backref("comments", lazy=True))


class Vote(db.Model):
    __tablename__ = "vote"

    post_id = db.Column(db.Integer, ForeignKey("post.post_id"), primary_key=True)
    account_id = db.Column(
        db.Integer, ForeignKey("account.account_id"), primary_key=True
    )
    value = db.Column(db.Integer, nullable=False)

    account = relationship("Account", backref=db.backref("votes", lazy=True))
    post = relationship("Post", backref=db.backref("votes", lazy=True))
