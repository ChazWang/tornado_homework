import tornado.web
from PIL import Image
import glob, os

from utils import photo
class IndexHandler(tornado.web.RequestHandler):
    '''图片分享首页'''
    def get(self, *args, **kwargs):
        images_path = os.path.join(self.settings.get('static_path'), 'uploads')
        print(images_path)
        images = photo.get_images(images_path)
        self.render('index.html', images=images)

class ExploreHandler(tornado.web.RequestHandler):
    '''所有图片展示'''
    def get(self, *args, **kwargs):
        self.render('explore.html')

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
            # img有三个键值对可以通过img.keys()查看
            # 分别是 'filename', 'body', 'content_type' 很明显对应着文件名,内容(二进制)和文件类型
            with open('./static/uploads/'+img['filename'], 'wb') as f:
                # 文件内容保存 到'/static/uploads/{{filename}}'
                f.write(img['body'])
                print('{}, 上传成功！'.format(img['filename']))
            self.write({'msg': 'got file: {}'.format(img_files[0]['filename'])})



