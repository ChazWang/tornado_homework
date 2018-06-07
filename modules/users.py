

from sqlalchemy import (Column, Integer, String)

from .db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    phone = Column(String(15))

    def __repr__(self):
        return '<User(#{}: {})>'.format(self.id, self.name)

if __name__ == '__main__':
    Base.metadata.create_all()

