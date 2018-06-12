import tornado.web
import glob, os
from pycket.session import SessionMixin
from PIL import Image

from utils.account import uploads, get_post_url

from utils import photo
class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tornado_user_info')

class PostHandler(tornado.web.RequestHandler):
    '''单个图片显示详情'''
    def get(self, post_id):
        self.render('post.html', post_id=post_id)

class IndexHandler(AuthBaseHandler):
    '''图片分享首页'''
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_url(self.current_user)
        images_url = [p.images_url for p in posts]
        self.render('index.html', images=images_url)
class ExploreHandler(AuthBaseHandler):
    '''所有图片展示'''
    def get(self, *args, **kwargs):
        posts = get_post_url(self.current_user)
        thumbs_url = [p.thumbs_url for p in posts]
        self.render('explore.html', images=thumbs_url)
class UploadHandler(AuthBaseHandler):
    # 接收图片上传文件
    def get(self, *args, **kwargs):
        self.render('upload.html')
    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg', None)
        # file_size = int(self.request.headers.get('Content-Length'))
        # if file_size / 1000.0 > 2000:
        #     self.write('上传的图片不能超过2M')
        for img in img_files:
            # 分别是 'filename', 'body', 'content_type' 很明显对应着文件名,内容(二进制)和文件类型
            base_name = 'uploads/' + img['filename']
            save_to = os.path.join(self.settings['static_path'], base_name)
            with open(save_to, 'wb') as f:
                f.write(img['body'])
                print('save to {}'.format(base_name))
            save_thumb_to = photo.get_thumbs(save_to)
            print('save to thumb {}'.format(save_thumb_to))
            save_thumb = os.path.relpath(save_thumb_to, self.settings['static_path'])
            uploads(self.current_user, base_name, save_thumb)
            self.write({'msg': 'got file: {}'.format(img_files[0]['filename'])})