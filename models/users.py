from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    orders = relationship("Order", backref='orders')
    favorites = relationship("Favorites", backref='favorites', uselist=False)

