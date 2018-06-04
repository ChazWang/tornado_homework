import glob
import os

def get_images(path):
    images = []
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

