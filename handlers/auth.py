from utils.account import authentication, register, login
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
            login(username)
            self.redirect('/')
        else:
            self.write('input error,login failed')
class LogOutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('tornado_user_info')
        self.redirect('/login')

class RegisterHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('register.html', msg='')
    def post(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        if username and password1 and password2:
            if password1 != password2:
                self.write('两次输入的密码不匹配')
            else:
                '''注册成功，直接跳转首页'''
                ret = register(username=username, password=password1, email=email)
                if ret['msg'] == 'ok':
                    self.session.set('tornado_user_info', username)
                    self.redirect('/')
                else:
                    self.write(ret)
        else:
            self.render('register.html', msg={'register fail'})
