import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    
    account_id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False)
    avatar_url = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=sa.func.current_timestamp())
    
    posts = relationship('Post', back_populates='account')

class Post(Base):
    __tablename__ = 'post'
    
    post_id = sa.Column(sa.Integer, primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.account_id'), nullable=False)
    title = sa.Column(sa.String(255), nullable=False)
    source = sa.Column(sa.String(255))
    score = sa.Column(sa.Integer, nullable=False)
    fav_count = sa.Column(sa.Integer, nullable=False)
    content = sa.Column(sa.TEXT, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=sa.func.current_timestamp())
    rating = sa.Column(sa.CHAR(1), nullable=False, default='g')
    
    account = relationship('Account', back_populates='posts')
    images = relationship('Image', back_populates='post')
    tags = relationship('Tag', secondary='post_tag', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    votes = relationship('Vote', back_populates='post')
    favorites = relationship('Favorite', back_populates='post')

class Image(Base):
    __tablename__ = 'image'
    
    image_id = sa.Column(sa.Integer, primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.post_id'), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    preview_url = sa.Column(sa.String(255), nullable=False)
    sample_url = sa.Column(sa.String(255), nullable=False)
    original_url = sa.Column(sa.String(255), nullable=False)
    width = sa.Column(sa.Integer)
    height = sa.Column(sa.Integer)
    
    post = relationship('Post', back_populates='images')

class Tag(Base):
    __tablename__ = 'tag'
    
    tag_id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Integer, nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    
    posts = relationship('Post', secondary='post_tag', back_populates='tags')

class PostTag(Base):
    __tablename__ = 'post_tag'
    
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.post_id'), primary_key=True)
    tag_id = sa.Column(sa.Integer, sa.ForeignKey('tag.tag_id'), primary_key=True)

class Comment(Base):
    __tablename__ = 'comment'
    
    comment_id = sa.Column(sa.Integer, primary_key=True)
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.post_id'), nullable=False)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('comment.comment_id'), default=None)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.account_id'), nullable=False)
    content = sa.Column(sa.TEXT, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, default=sa.func.current_timestamp())
    
    post = relationship('Post', back_populates='comments')
    account = relationship('Account')
    children = relationship('Comment', backref=sa.orm.backref('parent', remote_side=[comment_id]))

class Vote(Base):
    __tablename__ = 'vote'
    
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.post_id'), primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.account_id'), primary_key=True)
    value = sa.Column(sa.Integer, nullable=False)
    
    post = relationship('Post', back_populates='votes')
    account = relationship('Account')

class Favorite(Base):
    __tablename__ = 'favorite'
    
    post_id = sa.Column(sa.Integer, sa.ForeignKey('post.post_id'), primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.account_id'), primary_key=True)
    
    post = relationship('Post', back_populates='favorites')
    account = relationship('Account')