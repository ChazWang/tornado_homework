import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options, define

define('port', default=8000, help='run port', type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Python!!!')

application = tornado.web.Application(
    [
        (r'/', MainHandler),
    ],
    template_path='templates',
    static_path='static',
    debug=True,
)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()