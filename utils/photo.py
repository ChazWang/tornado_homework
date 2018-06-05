import glob
import os

from PIL import Image
def get_images(path):
    images = []
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

def get_thumbs(path):
    file, ext = os.path.splitext(os.path.basename(path))
    im = Image.open(path)
    im.thumbnail((200, 200))
    im.save("./static/uploads/thumbs/{}_{}x{}.jpg".format(file, 200 ,200), "JPEG")

