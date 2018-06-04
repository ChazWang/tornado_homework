import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    '''图片分享首页'''
    def get(self, *args, **kwargs):
        self.render('index.html')

class ExploreHandler(tornado.web.RequestHandler):
    '''所有图片展示'''
    def get(self, *args, **kwargs):
        self.render('explore.html')

class PostHandler(tornado.web.RequestHandler):
    '''单个图片显示详情'''
    def get(self, post_id):
        self.render('post.html', post_id=post_id)



