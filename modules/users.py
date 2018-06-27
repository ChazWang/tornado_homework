from datetime import datetime

from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship
from .db import Base, Session

session = Session() #实例化数据库操作
class User(Base):
    '''用户表'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    def __repr__(self):
        return '<User(#{}: {})>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls, username):
        '''判断用户是否存在于数据库中,返回布尔值'''
        return session.query(exists().where(User.name == username)).scalar()
    @classmethod
    def add_user(cls, username, password, email=''):
        '''创建用户写入到数据库'''
        user = User(name=username, password=password, email=email, last_login=datetime.now())
        session.add(user)
        session.commit()
    @classmethod
    def get_pass(cls, username):
        '''登陆判断用户名及密码'''
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user.password
        else:
            return ''
    @classmethod
    def update_time(cls, username):
        '''更新登陆时间'''
        login_time = datetime.now()
        # user_query = session.query(cls).filter_by(name=username)
        session.query(cls).filter_by(name=username).update({User.last_login: login_time})
        session.commit()
class Post(Base):
    '''用户图片关联信息'''
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    images_url = Column(String(80))
    thumbs_url = Column(String(80))
    user_id = Column(Integer, ForeignKey('users.id'))
    create_time = Column(DateTime, default=datetime.now)
    user = relationship('User', backref='posts', uselist=False, cascade='all')
    def __repr__(self):
        return '<Post(#{})>'.format(self.id)
    @classmethod
    def uploads_url(cls, username, images_url, thumbs_url):
        user = session.query(User).filter_by(name=username).first()
        post = Post(images_url=images_url, thumbs_url=thumbs_url, user=user)
        session.add(post)
        session.commit()
        return post
    @classmethod
    def get_url(cls, username):
        user = session.query(User).filter_by(name=username).first()
        posts = session.query(Post).order_by(Post.create_time.desc()).filter_by(user=user)
        return posts
    @classmethod
    def get_id(cls, id):
        return session.query(Post).filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return session.query(Post).order_by(Post.create_time.desc()).all()

class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)
    create_time = Column(DateTime, default=datetime.now)

if __name__ == '__main__':
    Base.metadata.create_all()

