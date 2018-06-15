import os
import uuid
from PIL import Image

class ImageSave(object):
    image_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200, 200)
    def __init__(self, static_path, file_name):
        self.static_path = static_path
        self.file_name = file_name
        self.new_name = self.uuid_name()

    def uuid_name(self):
        _, ext = os.path.splitext(self.file_name)
        return uuid.uuid4().hex + ext

    @property
    def images_url(self):
        return os.path.join(self.image_dir, self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path, self.images_url)

    def save_upload(self, content):  #上传写入到服务器
        with open(self.upload_path, 'wb') as f:
            f.write(content)

    @property
    def thumbs_url(self):
        file, _ = os.path.splitext(self.new_name)
        save_thumb = os.path.join(self.image_dir, self.thumb_dir,
                                  '{}_{}x{}.jpg'.format(file, self.size[0], self.size[1]))
        return save_thumb
    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(os.path.join(self.static_path, self.thumbs_url), "JPEG")



