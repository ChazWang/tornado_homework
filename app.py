import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options, define

from handlers import main, auth, chat
define('port', default=8000, help='run port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler),
            ('/login', auth.LoginHandler),
            ('/logout', auth.LogOutHandler),
            ('/register', auth.RegisterHandler),
            ('/room', chat.RoomHandler),
            ('/ws', chat.ChatSocketHandler),
            ('/profile', main.LikeHandler),
        ]
        settings = dict(
            template_path='templates',
            static_path='static',
            debug=True,
            login_url='/login',
            cookie_secret='fsf45875fdSDFaD58',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': '192.168.0.129',
                    # 'password': '',
                    'port': '6379',
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )
        super(Application, self).__init__(handlers, **settings)
        """
        super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。
        MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表
        """
application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Server start on port {}'.format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()