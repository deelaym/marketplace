from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from .database import Base


class Favorites(Base):
    __tablename__ = 'favorites'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)