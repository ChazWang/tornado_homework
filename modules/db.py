from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOSTNAME = '106.14.238.126'
PORT = '3306'
DATABASE = 'test'
USERNAME = 'root'
PASSWORD = 'beadwallet.mysql@2016'

Db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

engine = create_engine(Db_url)
Base = declarative_base(engine)
Session = sessionmaker(engine)

