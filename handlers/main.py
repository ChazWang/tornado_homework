import tornado.web
import os
from pycket.session import SessionMixin

from utils.account import uploads, get_post_url, get_post_id, get_post_all
from utils.photo import ImageSave

class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tornado_user_info')

class PostHandler(tornado.web.RequestHandler):
    '''单个图片显示详情'''
    def get(self, post_id):
        posts = get_post_id(post_id)
        self.render('post.html', posts=posts)

class IndexHandler(AuthBaseHandler):
    '''图片分享首页'''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_url(self.current_user)
        self.render('index.html', posts=posts)
class ExploreHandler(AuthBaseHandler):
    '''所有图片展示'''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_all()
        self.render('explore.html', posts=posts)
class UploadHandler(AuthBaseHandler):
    # 接收图片上传文件
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg', None)
        # file_size = int(self.request.headers.get('Content-Length'))
        # if file_size / 1000.0 > 2000:
        #     self.write('上传的图片不能超过2M')
        for img in img_files:
            image = ImageSave(self.settings['static_path'], img['filename'])
            image.save_upload(img['body'])  #保存上次的图片
            image.make_thumb()  #生成缩略图
            uploads(self.current_user, image.images_url, image.thumbs_url) #保存用户上传图片和缩略图的路径到数据库
        self.write({'msg': 'got file: {}'.format(img_files[0]['filename'])})
        self.redirect('/')