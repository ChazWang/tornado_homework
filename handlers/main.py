import tornado.web
import glob, os
from pycket.session import SessionMixin
from PIL import Image

from utils import photo
class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tornado_user_info')

class IndexHandler(AuthBaseHandler):
    '''图片分享首页'''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        images = photo.get_images('./static/uploads')
        self.render('index.html', images=images)

class ExploreHandler(tornado.web.RequestHandler):
    '''所有图片展示'''
    def get(self, *args, **kwargs):
        thumb_imgs = photo.get_images("./static/uploads/thumbs")
        self.render('explore.html',images = thumb_imgs)

class PostHandler(tornado.web.RequestHandler):
    '''单个图片显示详情'''
    def get(self, post_id):
        self.render('post.html', post_id=post_id)

class UploadHandler(tornado.web.RequestHandler):
    # 接收图片上传文件
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        # 这部分就是上传的文件,想要查看更多可以print self.request看看
        # 该文件返回一个元素为字典的列表
        img_files = self.request.files.get('newimg', None)
        file_size = int(self.request.headers.get('Content-Length'))
        if file_size / 1000.0 > 2000:
            self.write('上传的图片不能超过2M')
        for img in img_files:
            # 分别是 'filename', 'body', 'content_type' 很明显对应着文件名,内容(二进制)和文件类型
            with open('./static/uploads/'+img['filename'], 'wb') as f:
                f.write(img['body'])
                print('{}, 上传成功'.format(img['filename']))
            photo.get_thumbs('./static/uploads/'+img['filename'])
            print('{}, 缩略图生成成功'.format(img['filename']))
            self.write({'msg': 'got file: {}'.format(img_files[0]['filename'])})