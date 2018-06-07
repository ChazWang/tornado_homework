import tornado.web

from utils.account import authentication
from .main import AuthBaseHandler

class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        print(username, password)
        if authentication(username, password):
            self.session.set('tornado_user_info', username)
            self.redirect('/')
        else:
            self.write('login failed')

class LogOutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.set('tornado_user_info', '')
        self.redirect('/login')

class RegisterHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        if username and password1 and password2:
            if password1 != password2:
                self.write('两次输入的密码不匹配')
            else:
                pass
