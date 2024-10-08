import hashlib
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    __password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    orders = relationship("Order", backref='orders')
    favorites = relationship("Favorites", backref='favorites', uselist=False)

    @property
    def password(self):
        return None

    @password.setter
    def password(self, raw_password: str):
        h = hashlib.sha256()
        h.update(raw_password.encode())
        self.__password = h.hexdigest()

