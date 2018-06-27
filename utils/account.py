import hashlib

from modules.users import session
from modules.users import User, Post, Like

def hash_password(password):
    '''hash加密密码'''
    return hashlib.md5(password.encode('utf8')).hexdigest()
def authentication(username,password):
    '''登陆用户认证'''
    if username and password:
        hash_pass = User.get_pass(username)
        if hash_pass and hash_password(password) == hash_pass:
            return True
    return False
def login(username):
    '''更新最近一次登陆时间'''
    return User.update_time(username)
def register(username, password, email):
    '''判断用户是否已注册'''
    if User.is_exists(username):
        return {'msg': 'username is exists'}
    hash_pass = hash_password(password)
    User.add_user(username, hash_pass, email)
    return {'msg': 'ok'}
def uploads(username, images_url, thumbs_url):
    '''上传用户提交图片的url和缩略图url'''
    ret = Post.uploads_url(username=username, images_url=images_url, thumbs_url=thumbs_url)
    return ret
def get_post_url(username):
    posts = Post.get_url(username)
    return posts
def get_post_id(id):
    return Post.get_id(id)

def get_post_all():
    return Post.get_all()

def get_user(username):
    user = session.query(User).filter_by(name=username).first()
    return user

def get_like_users(post):
    '''图片有哪些用户喜欢'''
    users = session.query(User).filter(Like.post_id == post.id, Like.user_id == User.id).all()
    return users

def get_like_posts(user):
    '''查询用户喜欢的图片'''
    posts = session.query(Post).filter(Like.user_id == user.id, Like.post_id == Post.id, Post.user_id != user.id).all()
    print(posts)
    return posts