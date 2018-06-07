import hashlib

USER_DADA = {'username':'wang',
             'password': hashlib.md5('123'.encode()).hexdigest()}

def authentication(username,password):
    if username and password:
        passwd = hashlib.md5(password.encode()).hexdigest()
        if username == USER_DADA['username'] and passwd == USER_DADA['password']:
            return True
    return False
